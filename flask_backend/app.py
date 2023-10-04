import os
import uuid

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

from check import perform_code_check, perform_security_check

app = Flask(__name__)
app.secret_key = '123456'  # 设置会话密钥
app.config['UPLOAD_FOLDER'] = './usersfiles/'  # 设置文件上传目录
# 创建数据库连接和游标
conn = sqlite3.connect('users.db', check_same_thread=False)
cursor = conn.cursor()

# 创建用户表
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    );
''')

# 创建文件表
cursor.execute('''
    CREATE TABLE IF NOT EXISTS files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT NOT NULL,
        filepath TEXT NOT NULL,
        user_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES users (id)
    );
''')

conn.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET'])
def login():
    if 'user_id' in session:
        return redirect(url_for("dashboard"))
    else:
        return render_template('login.html')


@app.route('/dologin', methods=['POST'])
def dologin():
    if 'user_id' in session:
        return redirect(url_for("dashboard"))
    else:
        username = request.form['username']
        password = request.form['password']

        # 查询用户是否存在
        cursor.execute('SELECT * FROM users WHERE username=?', (username,))
        user = cursor.fetchone()

        if user and check_password_hash(user[2], password):
            # 用户存在且密码匹配，将用户id存储到会话中
            session['user_id'] = user[0]
            return redirect(url_for('dashboard'))
        else:
            # 用户不存在或密码不匹配，返回登录页面
            # 用户不存在或密码不匹配，返回登录页面并显示错误消息
            error_message = "用户名或密码错误"
            return render_template('login.html', error_message=error_message)


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' in session:
        user_id = session['user_id']
        # 查询用户信息
        cursor.execute('SELECT username FROM users WHERE id=?', (user_id,))
        username = cursor.fetchone()[0]
        # 查询用户关联的文件列表
        cursor.execute('SELECT filename, filepath FROM files WHERE user_id=?', (user_id,))
        files = [{'filename': f'第{i}次提交: '+filename[filename.index('_')+1:], 'filepath': filepath} for i, (filename, filepath) in enumerate(cursor.fetchall())]
        files.reverse()
        return render_template('dashboard.html', username=username, files=files)
    else:
        return redirect(url_for('login'))



@app.route('/docheak', methods=['POST'])
def docheak():
    if 'user_id' in session:
        selected_file = request.form['selected_file']
        cheak = request.form['cheak']
        if cheak == 'error_check':
            # 执行错误检查的逻辑
            result = "Error check result for " + selected_file
            return render_template('check_errors.html', result=result)
        elif cheak == 'security_check':
            # 执行安全检查的逻辑
            result = "Security check result for " + selected_file
            return render_template('security_check.html', result=result)
    else:
        return "no Authenticated"


@app.route('/logout')
def logout():
    # 从会话中移除用户id
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # 检查用户名是否已存在
        cursor.execute('SELECT * FROM users WHERE username=?', (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            # 用户名已存在，返回注册页面
            return redirect(url_for('register'))
        else:
            # 用户名不存在，将用户信息插入数据库
            hashed_password = generate_password_hash(password)
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
            conn.commit()

            # 注册成功后自动登录
            session['user_id'] = cursor.lastrowid
            return redirect(url_for('dashboard'))
    else:
        return render_template('register.html')


@app.route('/doupload', methods=['POST'])
def doupload():
    if 'user_id' in session:
        if 'file' not in request.files:
            # 没有选择文件
            return "No file selected"

        file = request.files['file']
        if file.filename == '':
            # 未选择文件
            return "No file selected"

        if file:
            # 生成唯一文件名
            filename = str(uuid.uuid4()) + '_' + file.filename
            # 保存文件到指定路径
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # 将文件信息存储在数据库中
            user_id = session.get('user_id')
            if user_id:
                filepath = app.config['UPLOAD_FOLDER']
                cursor.execute('INSERT INTO files (filename, filepath, user_id) VALUES (?, ?, ?)',
                               (filename, filepath, user_id))
                conn.commit()

                return redirect(url_for('dashboard'))
            else:
                return "User not logged in"
        else:
            return "File upload failed!"
    else:
        return "no Authenticated"

if __name__ == '__main__':
    app.run(threaded = True)