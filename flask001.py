from flask import Flask, url_for, render_template, request, redirect, g

from model import User

import sqlite3

app = Flask(__name__)
app.config["DATABASE"] = "database.db"


def connect_db():
    """Connects to the specific database."""
    db = sqlite3.connect(app.config['DATABASE'])
    return db


# 初始化数据库
def init_db():
    with app.app_context():
        db = connect_db()
        with app.open_resource('schema.sql', mode='r') as f:  # mode='r'只读模式 rb可读，可写
            db.cursor().executescript(f.read())  # 执行sql脚本
        db.commit()  # 提交sql表    commit 后断开连接数据库


@app.before_request
def before_request():
    # print('before_request')
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        # print('teardown_request')
        g.db.close()


def instert_user_to_db(users):
    sql_instert = "INSERT INTO users (name, pwd,email,age,birthday,face) values (?, ?, ?, ?, ?, ?)"  # 插入一条语句到users表中
    args = [users.name, users.pwd, users.email, users.age, users.birthday, users.face]
    g.db.execute(sql_instert, args)
    g.db.commit()


def query_users_from_db():
    users = []
    sql_select = "SELECT *FROM users"
    args = []
    cur = g.db.execute(sql_select, args)
    for item in cur.fetchall():
        user = User()
        # item[0] 为id
        user.name = item[1]
        user.pwd = item[2]
        user.email = item[3]
        user.age = item[4]
        user.birthday = item[5]
        user.face = item[6]
        users.append(user)
    return users
    pass


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/login/', methods=['GET', 'POST'])
def user_login():
    users = query_users_from_db()
    for user in users:
        print(user.name, user.pwd, user.email, user.birthday, user.age, user.face)
    return render_template("user_login.html")


@app.route('/regist/', methods=['GET', 'POST'])
def user_regist():
    if request.method == "POST":
        # print(request.form)
        user = User()
        user.name = request.form["user_name"]
        user.pwd = request.form["user_pwd"]
        user.age = request.form["user_age"]
        user.birthday = request.form["user_birthday"]
        user.email = request.form["user_email"]
        user.face = request.form["user_face"]

        instert_user_to_db(user)

        # username作为查询参数带到url中去
        ## 重定向页面 生成url 执行 user_login 函数 跳转到登录界面
        return redirect(url_for("user_login", username=user.name))
    return render_template("user_regist.html")


if __name__ == '__main__':
    app.run(debug=True)
