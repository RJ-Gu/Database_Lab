import mysql.connector
import json


# 连接数据库
def connect_db():
    try:
        cnx = mysql.connector.connect(
            host='localhost',
            user='root',
            password='oliver',
            database='lab02'
        )
        return cnx
    except Exception as e:
        print(e)
        return None


# 查询数据库
def query_db(query):
    cnx = connect_db()
    cursor = cnx.cursor()
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        cnx.close()
        return True, result
    except Exception as e:
        print(e)
        cursor.close()
        cnx.close()
        return False, None


def modify_db(query):
    cnx = connect_db()
    cursor = cnx.cursor()
    try:
        cursor.execute(query)
        cnx.commit()
        cursor.close()
        cnx.close()
        return True
    except Exception as e:
        print(e)
        cursor.close()
        cnx.close()
        return False


# 调用存储方法
def call_db_proc(procname: str, param_tuple: tuple):
    cnx = connect_db()
    cursor = cnx.cursor()
    try:
        cursor.callproc(procname, param_tuple)
        cnx.commit()
        cursor.close()
        cnx.close()
        return True
    except Exception as e:
        print(e)
        cursor.close()
        cnx.close()
        return False


# 通过用户名和密码检查用户是否存在
def check_user(username: str, password: str):
    query = "SELECT * FROM users WHERE username = '{}' AND password = '{}'".format(username, password)
    err, result = query_db(query)
    if err is False:
        return False
    if result == []:
        return False
    else:
        return True


# 通过用户名获取学生id（user表查询）
def get_student_id(username: str):
    query = "SELECT student_id FROM users WHERE username = '{}'".format(username)
    err, result = query_db(query)
    if err:
        return result[0][0]
    else:
        return None


# 注册用户
def register_user(username: str, password: str, student_id: int):
    query = "SELECT * FROM users WHERE username = '{}'".format(username)
    err, result = query_db(query)
    if err is False:
        return False
    if result != []:
        return False
    # Insert new user
    query = "INSERT INTO users (username, password, student_id) VALUES ('{}', '{}', {})".format(username, password,
                                                                                                student_id)
    return modify_db(query)


# 获取学生信息列表
# 包括：学号、姓名、性别、身份证号、电话、民族、籍贯、学历、专业号、专业名称、所属院系
def get_student_info_list(student_id: int):
    def get_extended_info_dict(student_id: int):
        query = "SELECT * FROM student WHERE sno = {}".format(student_id)
        err, result = query_db(query)
        if err is False:
            return None
        student_basic_info_tuple = result[0]
        keys = ('id', 'name', 'gender', 'id_card', 'phone', 'ethnicity', 'city', 'education', 'major_no')
        student_basic_info_dict = dict(zip(keys, student_basic_info_tuple))
        major_no = student_basic_info_dict['major_no']
        # 根据major_no查询专业名称以及所属院系
        query = ("SELECT student.smajor, major.mname, college.cname, college.cno "
                 "FROM student, major, college "
                 "WHERE student.smajor = major.mno "
                 "AND major.mcollege = college.cno "
                 "AND student.smajor = {}".format(major_no))
        err, result = query_db(query)
        if err is False:
            return None
        student_extended_info_tuple = result[0]
        # print(student_extended_info_tuple)
        student_info_dict = student_basic_info_dict
        student_info_dict['major'] = student_extended_info_tuple[1]
        student_info_dict['college'] = student_extended_info_tuple[2]
        student_info_dict['college_no'] = student_extended_info_tuple[3]
        return student_info_dict

    # root用户，可以访问所有学生信息
    if student_id == 0:
        query = "SELECT student.sno FROM student"
        err, result = query_db(query)
        if err is False:
            return None
        student_ids = [x[0] for x in result]
        student_info_list = []
        for student_id in student_ids:
            student_info_dict = get_extended_info_dict(student_id)
            student_info_list.append(student_info_dict)
        return student_info_list
    else:
        return [get_extended_info_dict(student_id)]


def get_full_course_info_list():
    query = "SELECT * FROM course"
    err, result = query_db(query)
    if err is False:
        return None
    course_list = []
    for course_tuple in result:
        course_dict = {
            'id': course_tuple[0],  # 课程号
            'name': course_tuple[1],  # 课程名
            'college_no': course_tuple[2],  # 专业号
            'major_no': course_tuple[3],  # 院系号
            'credit': course_tuple[4],  # 学分
            'full_time': course_tuple[5],  # 学时
            'type': course_tuple[6],  # 课程类型
            'time': course_tuple[7],  # 上课时间
            'location': course_tuple[8],  # 上课地点
        }
        course_list.append(course_dict)

    # 查询专业名称
    for course_dict in course_list:
        major_no = course_dict['major_no']
        query = "SELECT mname FROM major WHERE mno = {}".format(major_no)
        err, result = query_db(query)
        if err is False:
            return None
        course_dict['major'] = result[0][0]

    # 查询院系名称
    for course_dict in course_list:
        college_no = course_dict['college_no']
        query = "SELECT cname FROM college WHERE cno = {}".format(college_no)
        err, result = query_db(query)
        if err is False:
            return None
        course_dict['college'] = result[0][0]

    # 查询上课老师
    for course_dict in course_list:
        course_id = course_dict['id']
        # 一门课可能有多个老师
        query = ("SELECT teacher.tname "
                 "FROM teacher, teacher_course "
                 "WHERE teacher.tno = teacher_course.tno "
                 "AND teacher_course.cno = {}".format(course_id))
        err, result = query_db(query)
        if err is False:
            return None
        teachers = [x[0] for x in result]
        course_dict['teachers'] = teachers
    return course_list


def get_my_course_info_list(student_id: int):
    if student_id != 0:
        query = ("SELECT course.cno, course.cname, course.ccredit, student_course.grade, student_course.gpa "
                 "FROM course, student_course "
                 "WHERE course.cno = student_course.cno "
                 "AND student_course.sno = {}".format(student_id))
    else:
        query = ("SELECT course.cno, course.cname, course.ccredit, student_course.grade, student_course.gpa "
                 "FROM course, student_course "
                 "WHERE course.cno = student_course.cno")
    err, result = query_db(query)
    if err is False:
        return None
    my_course_info_list = []
    for course_tuple in result:
        course_dict = {
            'id': course_tuple[0],
            'name': course_tuple[1],
            'credit': course_tuple[2],
            'grade': course_tuple[3],
            'gpa': course_tuple[4]
        }
        my_course_info_list.append(course_dict)
    return my_course_info_list


def get_reward_punishment_list(student_id: int):
    if student_id != 0:
        query = ("SELECT student.sno, student.sname, reward_punish.rcontent, reward_punish.rtype "
                 "FROM student, reward_punish, student_reward_punish "
                 "WHERE reward_punish.rno = student_reward_punish.rno "
                 "AND student.sno = student_reward_punish.sno "
                 "AND student_reward_punish.sno = {}".format(student_id))
    else:
        query = ("SELECT student.sno, student.sname, reward_punish.rcontent, reward_punish.rtype "
                 "FROM student, reward_punish, student_reward_punish "
                 "WHERE reward_punish.rno = student_reward_punish.rno "
                 "AND student.sno = student_reward_punish.sno")
    err, result = query_db(query)
    if err is False:
        return None
    reward_punishment_list = []
    for reward_punishment_tuple in result:
        reward_punishment_dict = {
            'id': reward_punishment_tuple[0],
            'name': reward_punishment_tuple[1],
            'content': reward_punishment_tuple[2],
            'type': reward_punishment_tuple[3]
        }
        reward_punishment_list.append(reward_punishment_dict)
    return reward_punishment_list


def get_full_course_grade_info_list(student_id: int):
    if student_id != 0:
        return None
    query = "SELECT * FROM student_course"
    err, result = query_db(query)
    if err is False:
        return None
    full_course_grade_info_list = []
    for course_grade_tuple in result:
        course_grade_dict = {
            'student_id': course_grade_tuple[0],
            'course_id': course_grade_tuple[1],
            'grade': course_grade_tuple[2],
            'gpa': course_grade_tuple[3]
        }
        full_course_grade_info_list.append(course_grade_dict)
    # 查询课程名称
    for course_grade_dict in full_course_grade_info_list:
        course_id = course_grade_dict['course_id']
        query = "SELECT cname FROM course WHERE cno = {}".format(course_id)
        err, result = query_db(query)
        if err is False:
            return None
        course_grade_dict['course_name'] = result[0][0]
    # 查询学生姓名
    for course_grade_dict in full_course_grade_info_list:
        student_id = course_grade_dict['student_id']
        query = "SELECT sname FROM student WHERE sno = {}".format(student_id)
        err, result = query_db(query)
        if err is False:
            return None
        course_grade_dict['student_name'] = result[0][0]
    return full_course_grade_info_list


def get_full_college_major_info_list():
    query = "SELECT * FROM college"
    err, result = query_db(query)
    if err is False:
        return None
    college_list = []
    for college_tuple in result:
        college_dict = {
            'id': college_tuple[0],
            'name': college_tuple[1],
            'major': []
        }
        query = "SELECT * FROM major WHERE mcollege = {}".format(college_tuple[0])
        err, result = query_db(query)
        if err is False:
            return None
        for major_tuple in result:
            major_dict = {
                'id': major_tuple[0],
                'name': major_tuple[1]
            }
            college_dict['major'].append(major_dict)
        college_list.append(college_dict)
    return college_list


def update_student_info(new_student_info: dict):
    # 生成传输给sql的参数列表
    param_tuple = (
        new_student_info['id'], new_student_info['name'], new_student_info['gender'], new_student_info['id_card'],
        new_student_info['phone'], new_student_info['ethnicity'], new_student_info['city'],
        new_student_info['education'])

    result = call_db_proc('edit_student_info', param_tuple)
    if result is True:
        return True
    else:
        return False


def major_change(new_major_change_info: dict):
    # 生成传输给sql的参数列表
    param_tuple = (new_major_change_info['student_id'], new_major_change_info['major_id'])
    result = call_db_proc('major_change', param_tuple)
    if result is True:
        return True
    else:
        return False


def get_student_total_gpa(student_id: int):
    query = "SELECT calculate_student_total_gpa({});".format(student_id)
    err, result = query_db(query)
    if err is False:
        return None
    return result[0][0]


if __name__ == "__main__":
    result = get_student_total_gpa(10001)
    print(result)
