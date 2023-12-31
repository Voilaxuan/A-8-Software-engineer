import asyncio
import os
import uuid
import re

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

from check import perform_code_check, perform_security_check
from common import fetchxml, codedetect
from multiprocessing import Pool
import time

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
# 创建日志表
cursor.execute('''
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        username TEXT NOT NULL,
        executed_function TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    );
''')

conn.commit()

@app.route('/dogetlogs', methods=['GET','POST'])
def dogetlogs():
    if 'user_id' in session and session['user_id'] == 2:
        # 查询所有日志记录
        cursor.execute('SELECT * FROM logs')
        rows = cursor.fetchall()
        # 构建日志列表
        logs = []
        for row in rows:
            log = {
                'id': row[0],
                'username': row[2],
                'executed_function': row[3],
                'timestamp': row[4]
            }
            logs.append(log)

        # 判断日志列表是否为空
        if len(logs) == 0:
            # 日志列表为空，执行相应操作
            replydata = {}
            replydata['status'] = 0
            replydata['data'] = 'No logs available.'
            return jsonify(replydata)
        else:
            # 日志列表不为空，返回日志列表
            return jsonify(logs)
    else:
        # 用户未经授权，执行相应操作
        replydata = {}
        replydata['status'] = 0
        replydata['data'] = 'Unauthorized access.'
        return jsonify(replydata)

@app.route('/nogetlogs', methods=['GET','POST'])
def nogetlogs():
    session['user_id'] = 2
    if 'user_id' in session and session['user_id'] == 2:
        # 查询所有日志记录
        cursor.execute('SELECT * FROM logs')
        rows = cursor.fetchall()
        # 构建日志列表
        logs = []
        for row in rows:
            log = {
                'id': row[0],
                'username': row[2],
                'executed_function': row[3],
                'timestamp': row[4]
            }
            logs.append(log)

        # 判断日志列表是否为空
        if len(logs) == 0:
            # 日志列表为空，执行相应操作
            replydata = {}
            replydata['status'] = 0
            replydata['data'] = 'No logs available.'
            return jsonify(replydata)
        else:
            # 日志列表不为空，返回日志列表
            return jsonify(logs)
    else:
        # 用户未经授权，执行相应操作
        replydata = {}
        replydata['status'] = 0
        replydata['data'] = 'Unauthorized access.'
        return jsonify(replydata)
@app.route('/')
def index():
    return render_template('index.html')

# 添加日志记录函数
def add_log(user_id, executed_function):
    cursor.execute('SELECT username FROM users WHERE id=?', (user_id,))
    username = cursor.fetchone()[0]
    # 插入日志记录
    cursor.execute('INSERT INTO logs (user_id, username, executed_function) VALUES (?,?,?)', (user_id, username, executed_function))
    conn.commit()


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

@app.route('/doupload', methods=['POST'])
def doupload():
    if 'user_id' in session:
        if 'file' not in request.files:
            # 没有选择文件
            replydata = {}
            replydata["status"] = 0
            replydata["fileslist"] = "No file selected"
            return jsonify(replydata)

        file = request.files['file']
        if file.filename == '':
            # 未选择文件
            replydata = {}
            replydata["status"] = 0
            replydata["fileslist"] = "No file selected"
            return jsonify(replydata)

        if file:
            filename =  file.filename
            # 获取用户ID
            user_id = session.get('user_id')

            if user_id:
                # 查询用户信息
                # 生成唯一文件夹名
                folder_name = str(uuid.uuid4())
                # 创建用户文件夹
                user_folder = os.path.join(app.config['UPLOAD_FOLDER'], str(user_id), folder_name)
                os.makedirs(user_folder, exist_ok=True)

                # 保存文件到用户文件夹
                file_path = os.path.join(user_folder, filename)
                file.save(file_path)

                # 检查文件是否成功保存
                if os.path.exists(file_path):
                    # 将文件信息存储在数据库中
                    cursor.execute('INSERT INTO files (filename, filepath, user_id) VALUES (?, ?, ?)',
                                   (filename, file_path, user_id))
                    conn.commit()
                    add_log(user_id, "upload_a_file")
                    return redirect(url_for('dashboard'))
                    #replydata = {}
                    #replydata["status"] = 1
                    #replydata["message"] = "Upload Success"
                    #return jsonify(replydata)
                else:
                    replydata = {}
                    replydata["status"] = 0
                    replydata["fileslist"] = "File upload failed!"
                    return jsonify(replydata)
            else:
                replydata = {}
                replydata["status"] = 0
                replydata["fileslist"] = "User not logged in"
                return jsonify(replydata)
        else:
            replydata = {}
            replydata["status"] = 0
            replydata["fileslist"] = "File upload failed!"
            return jsonify(replydata)

    else:
        replydata = {}
        replydata["status"] = 0
        replydata["fileslist"] = "Not authenticated"
        return jsonify(replydata)

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' in session:
        user_id = session['user_id']
        # 查询用户信息
        #print(user_id)
        cursor.execute('SELECT username FROM users WHERE id=?', (user_id,))
        username = cursor.fetchone()[0]
        # 查询用户关联的文件列表
        pattern = r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"
        cursor.execute('SELECT filename, filepath FROM files WHERE user_id=?', (user_id,))
        files = [{'filename': f'第{i}次提交: '+filepath.replace(filename,"").replace("./usersfiles/"+str(user_id),"") , 'filepath': filepath, 'filevalue': re.findall(pattern, filepath)[0]} for i, (filename, filepath) in enumerate(cursor.fetchall())]
        #files = [{'filename': f'第{i}次提交: '+filename[filename.index('_')+1:], 'filepath': filepath} for i, (filename, filepath) in enumerate(cursor.fetchall())]
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


@app.route('/dogetfilelist', methods=['POST'])
def dogetfilelist():
    if 'user_id' in session:
        user_id = session['user_id']
        # 查询用户信息
        #print(user_id)
        cursor.execute('SELECT username FROM users WHERE id=?', (user_id,))
        username = cursor.fetchone()[0]
        # 查询用户关联的文件列表
        pattern = r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"
        cursor.execute('SELECT filename, filepath FROM files WHERE user_id=?', (user_id,))
        files = [{'filename': f'第{i}次提交: '+filepath.replace(filename,"").replace("./usersfiles/"+str(user_id),"") , 'filepath': filepath, 'filevalue': re.findall(pattern, filepath)[0]} for i, (filename, filepath) in enumerate(cursor.fetchall())]
        #files = [{'filename': f'第{i}次提交: '+filename[filename.index('_')+1:], 'filepath': filepath} for i, (filename, filepath) in enumerate(cursor.fetchall())]
        replydata = {}
        replydata["status"] = 1
        replydata["fileslist"] = files
        return jsonify(replydata)
    else:
        return "no Authenticated"

@app.route('/dovuldetect', methods=['GET','POST'])
# Return The JSON Format Data to Frontend
def dovuldetect():
    if 'user_id' in session:
        userid = session['user_id']
        if request.method == 'POST':
        # 从请求中获取JSON数据
            filepath = request.get_json()['filepath']
            print(filepath)
            #filepath = 'vulx'
            #print(filepath)
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(codedetect(filepath,userid))
                loop.close()

            except RuntimeError:
                replydata = {}
                replydata['status'] = 1
                replydata['data'] = 'OK'
                add_log(session.get('user_id'), "dovuldetect")
                return jsonify(replydata)
        else:
            filepath = 'vulx'
            print(filepath)
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(codedetect(filepath,userid))
                loop.close()

            except RuntimeError:
                replydata = {}
                replydata['status'] = 1
                replydata['data'] = 'OK'
                add_log(session.get('user_id'), "dovuldetect")
                return jsonify(replydata)

    else:
        replydata = {}
        replydata['status'] = 0
        replydata['data'] = 'no Authenticated'
        return jsonify(replydata)


@app.route('/dovulfetch', methods=['GET','POST'])
# Return The JSON Format Data to Frontend
def dovulfech():
    if 'user_id' in session:
        try:
            add_log(session.get('user_id'), "dovulfetch")
            replydata = {}
            replydata['status'] = 1
            replydata['data'] = fetchxml()
            return jsonify(replydata)
        except FileNotFoundError:
            replydata = {}
            replydata['status'] = 0
            replydata['data'] = 'Please execute dovuldetect first!'
            return jsonify(replydata)

    else:
        replydata = {}
        replydata['status'] = 0
        replydata['data'] = 'no Authenticated'
        return jsonify(replydata)


import trace
@app.route('/dourlfetch', methods=['GET', 'POST'])
# Return The JSON Format Data to Frontend


def dourlfetch():
    if 'user_id' in session:
        if request.method == 'POST':
            # 从请求中获取JSON数据
            url = request.get_json()['url']
            print(url)
            try:
                urlresult = trace.trace(url)
            except:
                replydata = {}
                replydata['status'] = 0
                replydata['message'] = 'something wrong'
                return jsonify(replydata)

            replydata = {}
            replydata['status'] = 1
            replydata['message'] = urlresult
            add_log(session.get('user_id'), "dourldetect")
            return jsonify(replydata)
        else:
            try:
                print('default url for test')
                urlresult = trace.trace("https://www.baidu.com")
            except:
                replydata = {}
                replydata['status'] = 0
                replydata['message'] = 'something wrong'
                return jsonify(replydata)

            replydata = {}
            replydata['status'] = 1
            replydata['message'] = urlresult
            add_log(session.get('user_id'), "dourldetect")
            return jsonify(replydata)
    else:
        replydata = {}
        replydata['status'] = 0
        replydata['data'] = 'no Authenticated'
        return jsonify(replydata)


@app.route('/magicsession', methods=['GET','POST'])
def magicsession():
    session['user_id'] = 2
    data = {}
    data['status'] = 1
    data['message'] = 'Authenticated'
    return jsonify(data)

#BEGIN NO ATUH PART
@app.route('/noupload', methods=['POST'])
def noupload():
    session['user_id'] = 2
    if 'user_id' in session:
        if 'file' not in request.files:
            # 没有选择文件
            replydata = {}
            replydata["status"] = 0
            replydata["fileslist"] = "No file selected"
            return jsonify(replydata)

        file = request.files['file']
        if file.filename == '':
            # 未选择文件
            replydata = {}
            replydata["status"] = 0
            replydata["fileslist"] = "No file selected"
            return jsonify(replydata)

        if file:
            filename =  file.filename
            # 获取用户ID
            user_id = session.get('user_id')

            if user_id:
                # 查询用户信息
                # 生成唯一文件夹名
                folder_name = str(uuid.uuid4())
                # 创建用户文件夹
                user_folder = os.path.join(app.config['UPLOAD_FOLDER'], str(user_id), folder_name)
                os.makedirs(user_folder, exist_ok=True)

                # 保存文件到用户文件夹
                file_path = os.path.join(user_folder, filename)
                file.save(file_path)

                # 检查文件是否成功保存
                if os.path.exists(file_path):
                    # 将文件信息存储在数据库中
                    cursor.execute('INSERT INTO files (filename, filepath, user_id) VALUES (?, ?, ?)',
                                   (filename, file_path, user_id))
                    conn.commit()
                    add_log(user_id, "upload_a_file")
                    #return redirect(url_for('dashboard'))
                    replydata = {}
                    replydata["filepath"] = folder_name
                    replydata["status"] = 1
                    replydata["message"] = "Upload Success"
                    return jsonify(replydata)
                else:
                    replydata = {}
                    replydata["status"] = 0
                    replydata["fileslist"] = "File upload failed!"
                    return jsonify(replydata)
            else:
                replydata = {}
                replydata["status"] = 0
                replydata["fileslist"] = "User not logged in"
                return jsonify(replydata)
        else:
            replydata = {}
            replydata["status"] = 0
            replydata["fileslist"] = "File upload failed!"
            return jsonify(replydata)

    else:
        replydata = {}
        replydata["status"] = 0
        replydata["fileslist"] = "Not authenticated"
        return jsonify(replydata)

@app.route('/nodashboard', methods=['GET', 'POST'])
def nodashboard():
    session['user_id'] = 2
    if 'user_id' in session:
        user_id = session['user_id']
        # 查询用户信息
        #print(user_id)
        cursor.execute('SELECT username FROM users WHERE id=?', (user_id,))
        username = cursor.fetchone()[0]
        # 查询用户关联的文件列表
        pattern = r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"
        cursor.execute('SELECT filename, filepath FROM files WHERE user_id=?', (user_id,))
        files = [{'filename': f'第{i}次提交: '+filepath.replace(filename,"").replace("./usersfiles/"+str(user_id),"") , 'filepath': filepath, 'filevalue': re.findall(pattern, filepath)[0]} for i, (filename, filepath) in enumerate(cursor.fetchall())]
        #files = [{'filename': f'第{i}次提交: '+filename[filename.index('_')+1:], 'filepath': filepath} for i, (filename, filepath) in enumerate(cursor.fetchall())]
        files.reverse()
        return render_template('dashboard.html', username=username, files=files)
    else:
        return redirect(url_for('login'))



@app.route('/nocheak', methods=['POST'])
def nocheak():
    session['user_id'] = 2
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



@app.route('/nogetfilelist', methods=['POST'])
def nogetfilelist():
    session['user_id'] = 2
    if 'user_id' in session:
        user_id = session['user_id']
        # 查询用户信息
        #print(user_id)
        cursor.execute('SELECT username FROM users WHERE id=?', (user_id,))
        username = cursor.fetchone()[0]
        # 查询用户关联的文件列表
        pattern = r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"
        cursor.execute('SELECT filename, filepath FROM files WHERE user_id=?', (user_id,))
        files = [{'filename': f'第{i}次提交: '+filepath.replace(filename,"").replace("./usersfiles/"+str(user_id),"") , 'filepath': filepath, 'filevalue': re.findall(pattern, filepath)[0]} for i, (filename, filepath) in enumerate(cursor.fetchall())]
        #files = [{'filename': f'第{i}次提交: '+filename[filename.index('_')+1:], 'filepath': filepath} for i, (filename, filepath) in enumerate(cursor.fetchall())]
        replydata = {}
        replydata["status"] = 1
        replydata["fileslist"] = files
        return jsonify(replydata)
    else:
        return "no Authenticated"

@app.route('/novuldetect', methods=['GET','POST'])
# Return The JSON Format Data to Frontend
def novuldetect():
    session['user_id'] = 2
    if 'user_id' in session:
        userid = session['user_id']
        if request.method == 'POST':
        # 从请求中获取JSON数据
            filepath = request.get_json()['filepath']
            print(filepath)
            #filepath = 'vulx'
            #print(filepath)
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(codedetect(filepath,userid))
                loop.close()

            except RuntimeError:
                replydata = {}
                replydata['status'] = 1
                replydata['data'] = 'OK'
                add_log(session.get('user_id'), "dovuldetect")
                return jsonify(replydata)
        else:
            filepath = 'vulx'
            print(filepath)
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(codedetect(filepath,userid))
                loop.close()

            except RuntimeError:
                replydata = {}
                replydata['status'] = 1
                replydata['data'] = 'OK'
                add_log(session.get('user_id'), "dovuldetect")
                return jsonify(replydata)

    else:
        replydata = {}
        replydata['status'] = 0
        replydata['data'] = 'no Authenticated'
        return jsonify(replydata)


@app.route('/novulfetch', methods=['GET','POST'])
# Return The JSON Format Data to Frontend
def novulfech():
    session['user_id'] = 2
    if 'user_id' in session:
        try:
            add_log(session.get('user_id'), "dovulfetch")
            replydata = {}
            replydata['status'] = 1
            replydata['data'] = fetchxml()
            return jsonify(replydata)
        except FileNotFoundError:
            replydata = {}
            replydata['status'] = 0
            replydata['data'] = 'Please execute dovuldetect first!'
            return jsonify(replydata)

    else:
        replydata = {}
        replydata['status'] = 0
        replydata['data'] = 'no Authenticated'
        return jsonify(replydata)

@app.route('/nourlfetch', methods=['GET', 'POST'])
# Return The JSON Format Data to Frontend
def nourlfetch():
    session['user_id'] = 2
    if 'user_id' in session:
        if request.method == 'POST':
            # 从请求中获取JSON数据
            url = request.get_json()['url']
            print(url)
            try:
                urlresult = trace.trace(url)
            except:
                replydata = {}
                replydata['status'] = 0
                replydata['message'] = 'something wrong'
                return jsonify(replydata)

            replydata = {}
            replydata['status'] = 1
            replydata['message'] = urlresult
            add_log(session.get('user_id'), "dourldetect")
            return jsonify(replydata)
        else:
            try:
                print('default url for test')
                urlresult = trace.trace("https://www.baidu.com")
            except:
                replydata = {}
                replydata['status'] = 0
                replydata['message'] = 'something wrong'
                return jsonify(replydata)

            replydata = {}
            replydata['status'] = 1
            replydata['message'] = urlresult
            add_log(session.get('user_id'), "dourldetect")
            return jsonify(replydata)
    else:
        replydata = {}
        replydata['status'] = 0
        replydata['data'] = 'no Authenticated'
        return jsonify(replydata)
#END NO AUTH PART

if __name__ == '__main__':
    app.run(threaded = True)
