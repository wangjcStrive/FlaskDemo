# -*- coding: utf-8 -*-
from flask import render_template, request, url_for, redirect, flash
from flask_login import login_user, login_required, logout_user, current_user

from watchlist import app, db
from watchlist.DataBase.DailyTaskDB import cursor, conn
from watchlist.models import User, Movie, ScoreRecord


def getAllRecord():
    allRecordList = []
    allRecord = cursor.execute("SELECT * FROM dbo.Daily ORDER BY ID DESC").fetchall()
    for eachRecord in allRecord:
        scoreRecordIns = ScoreRecord(eachRecord)
        allRecordList.append(scoreRecordIns)
    return allRecordList

def getRecordQuanty():
    sqlCount = 'SELECT COUNT(*) FROM [DailyTask].[dbo].[Daily]'
    return cursor.execute(sqlCount).fetchone()[0]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if not current_user.is_authenticated:
            return redirect(url_for('index'))

        title = request.form['title']
        year = request.form['year']

        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('index'))

        movie = Movie(title=title, year=year)
        db.session.add(movie)
        db.session.commit()
        flash('Item created.')
        return redirect(url_for('index'))

    movies = Movie.query.all()
    return render_template('index.html', movies=movies)

@app.route('/score', methods=['GET', 'POST'])
@login_required
def score():
    allRecordList = getAllRecord()
    allRecordCount = len(allRecordList)
    if request.method == 'POST':
        if not current_user.is_authenticated:
            return redirect(url_for('index'))
        emptyRecord = ScoreRecord()
        emptyRecord.id = getRecordQuanty() + 1
        return render_template('scoreEdit.html', score_record=emptyRecord)
    return render_template('score.html', scoreRecords=allRecordList, newRecordID=allRecordCount+1)


@app.route('/score/edit/<int:score_id>', methods=['GET', 'POST'])
@login_required
def score_edit(score_id):
    if request.method == 'POST':
        if not current_user.is_authenticated:
            return redirect(url_for('index'))
        sql_insert = 'INSERT INTO [DailyTask].[dbo].[Daily] ' \
                     'VALUES ({0}, \'{1}\', \'{2}\', {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}, {12}, {13}, {14}, \'{15}\', {16})'.format(
            request.form['ID'], request.form['date'], request.form['week'], request.form['baby'],
            request.form['earlyToBed'], request.form['drink'], request.form['jl'], request.form['eat'],
            request.form['washRoom'], request.form['coding'], request.form['learnDaily'], request.form['Eng'],
            request.form['efficiency'], request.form['hz'], request.form['score'], request.form['comments'],
            request.form['review'])
        cursor.execute(sql_insert)
        conn.commit()
        allRecordList = getAllRecord()
        return redirect(url_for('score'))
        # return render_template('score.html', scoreRecords=allRecordList)
    sql = 'SELECT * FROM dbo.Daily WHERE ID={}'.format(score_id)
    score_record_tuple = cursor.execute(sql).fetchone()
    if score_record_tuple != None:
        scoreRecordIns = ScoreRecord(score_record_tuple)
    else:
        scoreRecordIns =  ScoreRecord()
        scoreRecordIns.id = getRecordQuanty() + 1
    # print('\n'.join(['%s:%s' % item for item in score_record.__dict__.items()]))
    return render_template('scoreEdit.html', score_record = scoreRecordIns)


@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)

    if request.method == 'POST':
        title = request.form['title']
        year = request.form['year']

        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('edit', movie_id=movie_id))

        movie.title = title
        movie.year = year
        db.session.commit()
        flash('Item updated.')
        return redirect(url_for('index'))

    return render_template('edit.html', movie=movie)


@app.route('/movie/delete/<int:movie_id>', methods=['POST'])
@login_required
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('Item deleted.')
    return redirect(url_for('index'))


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']

        if not name or len(name) > 20:
            flash('Invalid input.')
            return redirect(url_for('settings'))

        user = User.query.first()
        user.name = name
        db.session.commit()
        flash('Settings updated.')
        return redirect(url_for('index'))

    return render_template('settings.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Invalid input.')
            return redirect(url_for('login'))

        user = User.query.first()

        if username == user.username and user.validate_password(password):
            login_user(user)
            flash('Login success.')
            return redirect(url_for('index'))

        flash('Invalid username or password.')
        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Goodbye.')
    return redirect(url_for('index'))