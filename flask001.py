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


# 往数据库插入数据
def instert_user_to_db(user):
    # sql_instert = "INSERT INTO users (name, pwd,email,age,birthday,face) VALUES (?, ?, ?, ?, ?, ?)"  # 插入一条语句到users表中

    # 构造  (name, pwd,email,age,birthday,face)
    user_attrs = user.getAttres()
    # 构造  “values (?, ?, ?, ?, ?, ?)"
    values = "VALUES("
    last_attr = user_attrs[-1]
    for attr in user_attrs:
        if attr != last_attr:
            values += "?,"
        else:
            values += "?"
    values += ")"
    sql_instert = "INSERT INTO users" + str(user_attrs) + values  # 插入一条语句到users表中

    # args = [user.name, user.pwd, user.email, user.age, user.birthday, user.face]
    args = user.tolist()
    g.db.execute(sql_instert, args)
    g.db.commit()


# 查询数据库所有数据
def query_users_from_db():
    users = []
    sql_select = "SELECT *FROM users"
    args = []
    cur = g.db.execute(sql_select, args)
    for item in cur.fetchall():
        user = User()
        # item[0] 为id
        # user.name = item[1]
        # user.pwd = item[2]
        # user.email = item[3]
        # user.age = item[4]
        # user.birthday = item[5]
        # user.face = item[6]

        user.fromList(item[1:])  # 第一位为id 从第二位才开始赋值

        users.append(user)
    return users
    pass


# 查询一条数据
def query_user_by_name(user_name):
    sql_select = "SELECT *FROM users WHERE name =?"
    args = [user_name]
    cur = g.db.execute(sql_select, args)
    items = cur.fetchall()  # 取出第一条数据
    if len(items) < 1:
        return None
    first_item = items[0]
    user = User()
    # item[0] 为id
    # user.name = first_item[1]
    # user.pwd = first_item[2]
    # user.email = first_item[3]
    # user.age = first_item[4]
    # user.birthday = first_item[5]
    # user.face = first_item[6]

    user.fromList(first_item[1:])  # 第一位为id 从第二位才开始赋值
    return user


# 按照条件（name）删除一条数据
def delete_user_by_name(user_name):
    dellete_sql = "DELETE FROM users WHERE name=?"  # DELETE FROM users 删除全部数据
    args = [user_name]
    g.db.execute(dellete_sql, args)
    g.db.commit()


@app.route('/')
def index():
    delete_user_by_name("123")
    return render_template("index.html")


@app.route('/login/', methods=['GET', 'POST'])
def user_login():
    users = query_users_from_db()
    for user in users:
        print(user.tolist())
    print("==========================")
    user_one = query_user_by_name("123")
    if user_one:
        print(user_one.tolist())
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
