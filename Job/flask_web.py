from flask import Flask, render_template, url_for, flash, redirect, request

from Job.forms import RoomForm
from Job.flask_crawler import get_crawler_result
from flask import jsonify

app = Flask(__name__)

app.config['SECRET_KEY'] = 'e4dda8aeb727af814f0713ebd476c92a'

posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jerry Huang',
        'title': 'Blog post 2',
        'content': 'Second post content',
        'date_posted': 'April 20, 2019'
    }
]


@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


# return "<h1>About page</h1>"


# http://127.0.0.1:5000/room?url=https://www.lesaintsulpice.com/en/our-suites/deluxe-suite
@app.route("/")
@app.route("/room", methods=['GET', 'POST'])
def room():
    form = RoomForm()

    url = request.args.get('url')
    print(url)
    form.roomid.data = url
    dict_result = get_crawler_result(url)
    print('jsonify(dict_result) == ', jsonify(dict_result))
    form.roomname.data = dict_result['roomType']
    form.bedtype.data = dict_result['bedType']
    form.roomclass.data = dict_result['roomClass']
    form.roomsize.data = dict_result['roomSize']

    if form.validate_on_submit():
        flash(f'Account created for {form.roomid.data}!', 'success')
        return redirect(url_for("room"))
    return render_template('room.html', title='Room', form=form)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
