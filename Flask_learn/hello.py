from flask import Flask
from flask import request

# 方法来渲染模板
# 将模板名和你想作为关键字的参数传入模板的变量
from flask import render_template

app = Flask(__name__)

# 打开调试模式：启用了调试支持，服务器会在代码修改后自动重新载入，并在发生错误时提供一个相当有用的调试器
app.run(debug=True)

#
# @app.route("/", methods=['GET', 'POST'])
# def hello():
#     return "hello world"

@app.route('/index/')
@app.route('/index/<name>')
def index(name=None):
    return render_template('index.html', name=name)


@app.route('/hello/')
@app.route('/hello/<name>')
def hello_temple(name=None):
    return render_template('hello.html', name=name)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

# @app.route('/login', methods=['POST', 'GET'])
# def login():
#     error = None
#     if request.method == 'POST':
#         if valid_login(request.form['username'],
#                        request.form['password']):
#             return log_the_user_in(request.form['username'])
#         else:
#             error = 'Invalid username/password'
#     # the code below is executed if the request method
#     # was GET or the credentials were invalid
#     return render_template('login.html', error=error)


if __name__ == '__main__':
    app.run()