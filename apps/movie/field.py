from flask_restful import fields

# 分页数据
#
from apps.main.field import IndexFields

pag_fields = {
    'pages':fields.Integer,
    'total':fields.Integer,
}

data_fields = {
    'pagination':fields.Nested(pag_fields),
    'movies':fields.List(fields.Nested(IndexFields.movie_fields))
}





# 电影详情结构
class MovieDetailFields:

    area_fields = {
        'aid':fields.Integer,
        'name':fields.String
    }
    cinemas_fields = {
        'cid': fields.Integer,
        'name': fields.String,

    }
    hall_fields = {
        'hid': fields.Integer,
        'name': fields.String,
        'screen_type': fields.Integer,
        'seat_num': fields.Integer
    }
    hs_fields = {
        'hsid': fields.Integer,
        'start': fields.String,
        'end': fields.String,
        'origin_price': fields.Float,
        'current_price': fields.Float,
        'status': fields.Integer,
        'hall': fields.Nested(hall_fields)
    }
    data_fields = {
        'movie':fields.Nested(IndexFields.movie_fields),
        'area':fields.List(fields.Nested(area_fields)),
        'cinema':fields.List(fields.Nested(cinemas_fields)),
        'hallschedul':fields.List(fields.Nested(hs_fields))
    }
    result_fields = {
        'status': fields.Integer(default=200),
        'msg': fields.String(default='success'),
        'data': fields.Nested(data_fields)
    }



class MoviesFields:
    result_fields = {
        'status': fields.Integer,
        'msg': fields.String,
        'data':fields.Nested(data_fields)
    }