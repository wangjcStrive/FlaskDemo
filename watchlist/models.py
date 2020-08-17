# -*- coding: utf-8 -*-
import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from watchlist import db
from time import time, localtime, strftime


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))


class ScoreRecord(db.Model):
    def __init__(self, *record):
        if len(record) == 0:
            self.date = datetime.datetime.now().strftime('%Y-%m-%d')
            self.week = strftime("%a", localtime(time()))
            self.baby = 0
            self.EarlyToBed = 0
            self.Drink = 0
            self.JL = 0
            self.Eat = 0
            self.WashRoom = 0
            self.Coding = 0
            self.LearnDaily = 0
            self.Eng = 0
            self.Efficiency = 0
            self.HZ = 0
            self.Score = 0
            self.Comments = ' '
            self.Review = 0
        else:
            self.id = record[0][0]
            self.date = record[0][1]
            self.week = record[0][2]
            self.baby = record[0][3]
            self.EarlyToBed = record[0][4]
            self.Drink = record[0][5]
            self.JL = record[0][6]
            self.Eat = record[0][7]
            self.WashRoom = record[0][8]
            self.Coding = record[0][9]
            self.LearnDaily = record[0][10]
            self.Eng = record[0][11]
            self.Efficiency = record[0][12]
            self.HZ = record[0][13]
            self.Score = record[0][14]
            self.Comments = record[0][15]
            self.Review = record[0][16]

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20))
    week = db.Column(db.String(20))
    baby = db.Column(db.Integer)
    EarlyToBed = db.Column(db.Integer)
    JL = db.Column(db.Integer)
    Drink = db.Column(db.Integer)
    Eat = db.Column(db.Integer)
    WashRoom = db.Column(db.Integer)
    Coding = db.Column(db.Integer)
    LearnDaily = db.Column(db.Integer)
    Eng = db.Column(db.Integer)
    Efficiency = db.Column(db.Integer)
    HZ = db.Column(db.Integer)
    Score = db.Column(db.Integer)
    Sports = db.Column(db.Integer)
    Comments = db.Column(db.Integer)
    Review = db.Column(db.Integer)