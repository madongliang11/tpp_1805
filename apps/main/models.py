import datetime

from apps.ext import db


class Area(db.Model):
    aid = db.Column(db.Integer, primary_key=True,autoincrement=True)
    parent_id = db.Column(db.Integer)
    short_name = db.Column(db.String(64),index=True)
    name = db.Column(db.String(64))
    merger_name = db.Column(db.String(64))
    level = db.Column(db.String(64))
    pinyin = db.Column(db.String(64))
    code = db.Column(db.String(64))
    zip_code = db.Column(db.String(64))
    first = db.Column(db.String(64))
    lng = db.Column(db.String(64))
    lat = db.Column(db.String(64))
    is_hot = db.Column(db.Integer)
    status = db.Column(db.Integer, default=False)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    show_name = db.Column(db.String(64), unique=True, index=True)
    show_name_en = db.Column(db.String(64))
    director = db.Column(db.String(32))
    leading_role = db.Column(db.String(256))
    type = db.Column(db.String(64))
    country = db.Column(db.String(32))
    language = db.Column(db.String(32))
    duration = db.Column(db.Integer)
    screening_model = db.Column(db.String(16))
    open_day = db.Column(db.Date)
    image = db.Column(db.String(256))
    flag = db.Column(db.Integer)
    is_delete = db.Column(db.Boolean, default=False)
    hs_list = db.relationship('HallScheduling',lazy='dynamic',backref='movie')




class Banner(db.Model):
    bid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100))
    image = db.Column(db.String(100))
    detail_url = db.Column(db.String(100))
    order = db.Column(db.Integer, default=0)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now())
    is_delete = db.Column(db.Boolean, default=False)


class Rating(db.Model):
    sid = db.Column(db.Integer,primary_key=True,autoincrement=True)
    score = db.Column(db.Float(3,1),default=0.0)
    movie_id = db.Column(db.Integer,db.ForeignKey(Movie.id,ondelete='CASCADE'))