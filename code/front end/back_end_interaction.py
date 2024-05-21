import mysql.connector


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
        query = ("SELECT student.smajor, major.mname, college.cname "
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


if __name__ == "__main__":
    result = get_student_info_list(10001)
    print(result)
