from flask import Flask, render_template, redirect, url_for, request
import back_end_interaction
import json
import os

app = Flask(__name__)


@app.route('/')
def first_page():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if back_end_interaction.check_user(username, password):
            student_id = back_end_interaction.get_student_id(username)
            return redirect(url_for('main_page', student_id=student_id))
        else:
            return '''
                <script>
                alert('用户名密码不正确！');
                window.location.href = "/";
                </script>
                '''
    else:
        return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        student_id = request.form['student-id']
        student_id = int(student_id)
        if back_end_interaction.register_user(username, password, student_id):
            return '''
                <script>
                alert('注册成功！');
                window.location.href = "/";
                </script>'''
        else:
            return '''
                <script>
                alert('用户名已经存在！');
                window.location.href = "/register";
                </script>
                '''
    else:
        return render_template('register.html')


# 主页面：root和个人用户均可访问
@app.route('/main_page')
def main_page():
    student_id = request.args.get('student_id', type=int)
    student_info_list = back_end_interaction.get_student_info_list(student_id)
    return render_template('main_page.html', student_id=student_id, student_info_list=student_info_list)


# 个人信息页面：个人用户可访问，root用户不访问
@app.route('/basic_info', methods=['GET', 'POST'])
def basic_info():
    if request.method == 'GET':
        student_id = request.args.get('student_id', type=int)
        student_info_list = back_end_interaction.get_student_info_list(student_id)
        return render_template('basic_info.html', student_id=student_id, student_info_list=student_info_list)
    else:  # POST
        try:
            student_id = request.form['student_id']
            image = request.files['image']
            print(student_id, image)
            # 保存图片
            image_path = os.path.join('static', 'student_images', '{}.jpg'.format(student_id))
            image.save(image_path)
            return """
            <script>
            alert('图片上传成功！');
            window.location.href = "/basic_info?student_id={}";
            </script>
            """.format(student_id)
        except Exception as e:
            student_id = request.form['student_id']
            print(e)
            return """
            <script>
            alert('图片上传失败！');
            window.location.href = "/basic_info?student_id={}";
            </script>
            """.format(student_id)


# 课程信息页面：root和个人用户均可访问
@app.route('/course_info')
def course_info():
    student_id = request.args.get('student_id', type=int)
    student_info_list = back_end_interaction.get_student_info_list(student_id)
    full_course_info_list = back_end_interaction.get_full_course_info_list()
    return render_template('course_info.html', student_id=student_id, student_info_list=student_info_list,
                           full_course_info_list=full_course_info_list)


# 个人课程信息页面：个人用户可访问，root用户不访问
@app.route('/my_course_info')
def my_course_info():
    student_id = request.args.get('student_id', type=int)
    student_info_list = back_end_interaction.get_student_info_list(student_id)
    my_course_info_list = back_end_interaction.get_my_course_info_list(student_id)
    return render_template('my_course_info.html', student_id=student_id, student_info_list=student_info_list,
                           my_course_info_list=my_course_info_list)


# 奖惩情况：root和个人用户均可访问
@app.route('/reward_punishment')
def reward_punishment():
    student_id = request.args.get('student_id', type=int)
    student_info_list = back_end_interaction.get_student_info_list(student_id)
    reward_punishment_list = back_end_interaction.get_reward_punishment_list(student_id)
    return render_template('reward_punishment.html', student_id=student_id, student_info_list=student_info_list,
                           reward_punishment_list=reward_punishment_list)


# 全部学生信息：root用户可访问，个人用户不访问
@app.route('/student_info', methods=['GET', 'POST'])
def student_info():
    if request.method == 'GET':
        student_id = request.args.get('student_id', type=int)
        student_info_list = back_end_interaction.get_student_info_list(0)
        return render_template('student_info.html', student_info_list=student_info_list, student_id=student_id)
    else:
        try:
            student_id = request.form['student_id']
            image = request.files['image']
            print(student_id, image)
            # 保存图片
            image_path = os.path.join('static', 'student_images', '{}.jpg'.format(student_id))
            image.save(image_path)
            return """
            <script>
            alert('图片上传成功！');
            window.location.href = "/student_info?student_id={}";
            </script>
            """.format(student_id)
        except Exception as e:
            student_id = request.form['student_id']
            print(e)
            return """
            <script>
            alert('图片上传失败！');
            window.location.href = "/student_info?student_id={}";
            </script>
            """.format(student_id)


# 全部课程与成绩信息：root用户可访问，个人用户不访问
@app.route('/course_grade_info')
def course_grade_info():
    full_course_grade_info_list = back_end_interaction.get_full_course_grade_info_list(0)
    print(full_course_grade_info_list)
    return render_template('course_grade_info.html', full_course_grade_info_list=full_course_grade_info_list)


@app.route('/edit_single_student_info', methods=['GET', 'POST'])
def edit_single_student_info():
    if request.method == 'GET':
        student_id = request.args.get('student_id', type=int)
        student_info_list = back_end_interaction.get_student_info_list(student_id)
        return render_template('edit_single_student_info.html', student_id=student_id,
                               student_info_list=student_info_list)
    else:
        new_student_id = request.args.get('student_id', type=int)
        new_student_name = request.form['name']
        new_student_gender = request.form['gender']
        new_student_id_card = request.form['id_card']
        new_student_phone = request.form['phone']
        new_student_ethnicity = request.form['ethnicity']
        new_student_city = request.form['city']
        new_student_education = request.form['education']
        new_student_info = {
            'id': new_student_id,
            'name': new_student_name,
            'gender': new_student_gender,
            'id_card': new_student_id_card,
            'phone': new_student_phone,
            'ethnicity': new_student_ethnicity,
            'city': new_student_city,
            'education': new_student_education
        }
        print(new_student_info)
        result = back_end_interaction.update_student_info(new_student_info)
        if result is True:
            # 更新成功
            return """
            <script>
            alert('更新成功！');
            window.location.href = "/main_page?student_id={}";
            </script>
            """.format(new_student_id)
        else:
            # 更新失败
            return """
            <script>
            alert('更新失败！');
            window.location.href = "/edit_single_student_info?student_id={}";
            </script>
            """.format(new_student_id)


@app.route('/change_major', methods=['GET', 'POST'])
def change_major():
    if request.method == 'GET':
        student_id = request.args.get('student_id', type=int)
        student_info_list = back_end_interaction.get_student_info_list(student_id)
        full_college_major_info_list = back_end_interaction.get_full_college_major_info_list()
        full_college_major_info_list_json = json.dumps(full_college_major_info_list)
        return render_template('change_major.html', student_id=student_id, student_info_list=student_info_list,
                               full_college_major_info_list=full_college_major_info_list_json)
    else:
        new_student_id = request.args.get('student_id', type=int)
        new_college_id = request.form['college']
        new_major_id = request.form['major']
        new_major_change_info = {
            'student_id': new_student_id,
            'college_id': new_college_id,
            'major_id': new_major_id
        }
        print(new_major_change_info)
        result = back_end_interaction.major_change(new_major_change_info)
        if result is True:
            # 更新成功
            return """
            <script>
            alert('转专业成功！');
            window.location.href = "/main_page?student_id={}";
            </script>
            """.format(new_student_id)
        else:
            # 更新失败
            return """
            <script>
            alert('转专业失败！');
            window.location.href = "/change_major?student_id={}";
            </script>
            """.format(new_student_id)


def image_exists(image_path):
    full_path = os.path.join('static', image_path)
    return os.path.exists(full_path)


@app.context_processor
def utility_processor():
    return dict(image_exists=image_exists)


if __name__ == '__main__':
    app.run()
