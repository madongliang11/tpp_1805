from flask_restful import fields

from apps.main.field import IndexFields


class CinemasFields:
    cinemas_fields = {
        'cid':fields.Integer,
        'name':fields.String,
        'address': fields.String,
        'phone': fields.String,
        'score': fields.Float,
    }
    result_fields = {
        'status': fields.Integer(default=200),
        'msg': fields.String(default='success'),
        'data': fields.List(fields.Nested(cinemas_fields))
    }


class AreaFields:
    district_fields = {
        'name': fields.String,
        'aid': fields.Integer
    }

    result_fields = {
        'status': fields.Integer(default=200),
        'msg': fields.String(default='success'),
        'data': fields.List(fields.Nested(district_fields))
    }


class CinemasDetauil:
    movie_list_fields = {
        'movie_id':fields.Integer,
        'show_name':fields.String,
    }
    hall_fields = {
        'hid':fields.Integer,
        'name':fields.String,
        'screen_type':fields.Integer,
        'seat_num':fields.Integer
    }
    hs_fields = {
        'hsid':fields.Integer,
        'start':fields.String,
        'end':fields.String,
        'origin_price':fields.Float,
        'current_price': fields.Float,
        'status':fields.Integer,
        'hall': fields.Nested(hall_fields)
    }
    data_fields = {
        # cinema模型对象
        'cinema':fields.Nested(CinemasFields.cinemas_fields),

        'movies': fields.List(fields.Nested(IndexFields.movie_fields)),
        # movie模型对象
        'movie':fields.Nested(IndexFields.movie_fields),
        #
        'hs_list':fields.List(fields.Nested(hs_fields))

    }
    result_fields = {
        'status': fields.Integer(default=200),
        'msg': fields.String(default='success'),
        'data': fields.Nested(data_fields)
    }