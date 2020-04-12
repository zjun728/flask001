from flask import Flask, url_for, render_template, request, redirect

app = Flask(__name__)


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
        print(request.form["user_name"])
        print(request.form["user_pwd"])
        print(request.form)
        return redirect(url_for("user_login"))  # 重定向页面 生成url 执行 user_login 函数 跳转到登录界面
    return render_template("user_regist.html")


if __name__ == '__main__':
    app.run(debug=True)
