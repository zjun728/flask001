from flask import Flask, url_for, render_template

app = Flask(__name__)


@app.route('/')
@app.route('/<name>')
def hello_world(name=None):
    # return 'Hello World!'
    print(name)
    # return render_template("index.html", name=name)
    user=['qq','q1','q2','q3','q4']
    return render_template("index.html", name=name,user=user)


@app.route('/post/<username>/<int:post_id>')
def show_post(username, post_id):
    return 'user %s post %d' % (username, post_id)


if __name__ == '__main__':
    app.run(debug=True)
    # with app.test_request_context():
    #     print(url_for('hello_world'))
    #     print(url_for('show_post', username='JohnDoe',post_id=123))
