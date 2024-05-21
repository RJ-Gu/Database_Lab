from flask import Flask, render_template, redirect, url_for, request
import back_end_interaction

app = Flask(__name__)


@app.route('/')
def first_page():
    return render_template('login.html')


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
        return redirect(url_for('first_page'))


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


@app.route('/main_page')
def main_page():
    student_id = request.args.get('student_id', type=int)
    student_info_list = back_end_interaction.get_student_info_list(student_id)
    return render_template('main_page.html', student_info_list=student_info_list)


if __name__ == '__main__':
    app.run()
