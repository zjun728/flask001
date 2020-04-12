from flask import Flask, url_for, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/regist/', methods=['GET', 'POST'])
def user_regist():
    return render_template("user_regist.html")


if __name__ == '__main__':
    app.run(debug=True)
