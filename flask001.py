from flask import Flask, url_for, render_template, request, redirect

from model import User

import sqlite3

app = Flask(__name__)
app.config["DATABASE"]="database.db"


def connect_db():
    """Connects to the specific database."""
    db = sqlite3.connect(app.config['DATABASE'])
    return db

#初始化数据库
def init_db():
    with app.app_context():
        db = connect_db()
        with app.open_resource('schema.sql', mode='r') as f:   # mode='r'只读模式 rb可读，可写
            db.cursor().executescript(f.read())    #执行sql脚本
        db.commit()   #提交sql表




@app.route('/')
def index():
    return render_template("index.html")


@app.route('/login/', methods=['GET', 'POST'])
def user_login():
    return render_template("user_login.html")


@app.route('/regist/', methods=['GET', 'POST'])
def user_regist():
    if request.method == "POST":
        print(request.form)
        user = User()
        user.name = request.form["user_name"]
        user.pwd = request.form["user_pwd"]
        user.age = request.form["user_age"]
        user.birthday = request.form["user_birthday"]
        user.email = request.form["user_email"]
        user.face = request.form["user_face"]
        print(user.name)

        # username作为查询参数带到url中去
        ## 重定向页面 生成url 执行 user_login 函数 跳转到登录界面
        return redirect(url_for("user_login", username=user.name))
    return render_template("user_regist.html")


if __name__ == '__main__':
    app.run(debug=True)
