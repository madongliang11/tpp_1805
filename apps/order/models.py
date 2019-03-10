import datetime

from apps.cinemas.models import Cinema, Hall, HallScheduling, SeatScheduling, Seats
from apps.ext import db
from apps.main.models import Movie


class Order(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    # 订单号
    no = db.Column(db.String(50), unique=True, index=True, nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey(Movie.id), nullable=False)
    cinema_id = db.Column(db.Integer, db.ForeignKey(Cinema.cid), nullable=False)
    hs_id = db.Column(db.Integer, db.ForeignKey(HallScheduling.hsid))
    ss_id = db.Column(db.Integer, db.ForeignKey(SeatScheduling.id))
    seat_id = db.Column(db.Integer, db.ForeignKey(Seats.sid))
    # 票数
    number = db.Column(db.Integer, nullable=False)
    # 取票码
    ticket_code = db.Column(db.String(100))
    # 总金额
    total = db.Column(db.Numeric(7, 2))
    #创建的时间
    create_date = db.Column(db.DateTime, default=datetime.datetime.now())
    pay_date = db.Column(db.DateTime)
    # 1 表示未支付 2 已支付, 3 表示支付已取票  4 表示支付未取票 5 退票
    status = db.Column(db.SmallInteger, nullable=False)
    # 有效期
    out_time = db.Column(db.DateTime, default=datetime.datetime.now()+datetime.timedelta(minutes=15))
    is_delete = db.Column(db.Boolean, default=False)
