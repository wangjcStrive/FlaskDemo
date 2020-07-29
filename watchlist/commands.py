# -*- coding: utf-8 -*-
import click

from watchlist import app, db
from watchlist.models import User, Movie, ScoreRecord


@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    """Initialize the database."""
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')


@app.cli.command()
def forge():
    """Generate fake data."""
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

    scoreRecord = [
        {'date': '20200701', 'week': 'Mon', 'baby': 1},
        {'date': '20200703', 'week': 'Thur', 'baby': 0},
        {'date': '20200705', 'week': 'Wed', 'baby': 1},
        {'date': '20200707', 'week': 'Tue', 'baby': 1},
        {'date': '20200709', 'week': 'Fri', 'baby': 1},
        {'date': '20200801', 'week': 'Sat', 'baby': 1},
        {'date': '20200901', 'week': 'Sun', 'baby': 1},
        {'date': '20201001', 'week': 'Mon', 'baby': 1},
        {'date': '20201101', 'week': 'Mon', 'baby': 1},
    ]

    # user = User(name=name)
    # db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)

    for n in scoreRecord:
        record = ScoreRecord(date=n['date'], week=n['week'], baby=n['baby'])
        db.session.add(record)

    db.session.commit()
    click.echo('Done.')



@app.cli.command()
@click.option('--username', prompt=True, help='The username used to login.')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login.')
def admin(username, password):
    """Create user."""
    db.create_all()

    user = User.query.first()
    if user is not None:
        click.echo('Updating user...')
        user.username = username
        user.set_password(password)
    else:
        click.echo('Creating user...')
        user = User(username=username, name='Admin')
        user.set_password(password)
        db.session.add(user)

    db.session.commit()
    click.echo('Done.')