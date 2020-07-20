import click
from flask import Flask, url_for, escape, render_template
from flask_sqlalchemy import SQLAlchemy
import  os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))


@app.route('/')
def index():
    user = User.query.first()
    movie = Movie.query.all()
    return render_template('index.html', movies=movie)

# binding the hello function to URL /
@app.route('/home')
def hello():
    return '<h1>Hello Totoro!</h1><img src="http://helloflask.com/totoro.gif">'

@app.route('/user/<name>')
def user_page(name):
    return 'User: %s' % escape(name)

@app.route('/test')
def test_url_for():
    print(url_for('hello'))
    print(url_for('user_page', name='jichen'))
    print(url_for('test_url_for'))
    return 'test page'

@app.errorhandler(404)
def page_not_found(e):
    user = User.query.first()
    return render_template('404.html'), 404  # 返回模板和状态码


# 多个模板内都需要使用的变量，用context_processon，会统一注入到每个模板的上下文环境中，可以在模板中直接使用
@app.context_processor
def inject_user():
    user = User.query.first()
    return dict(user=user)

# 注册为命令
# (env) $ flask initDB
@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initDB(drop):
    """initialize the database"""
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')

@app.cli.command()
def forge():
    db.create_all()
    name = 'Wangjc'
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]
    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)

    db.session.commit()
    click.echo('Done')