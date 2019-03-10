from flask_restful import fields




class IndexFields:
    banner_fields = {
        'bid': fields.Integer,
        'title': fields.String,
        'image': fields.String,
        'detail_url': fields.String,
    }
    movie_fields = {
        'id': fields.Integer,
        'show_name': fields.String,
        'show_name_en': fields.String,
        'director': fields.String,
        'leading_role': fields.String,
        'type': fields.String,
        'country': fields.String,
        'language': fields.String,
        'duration': fields.Integer,
        'screening_model': fields.String,
        'image':fields.String,
        'open_day':fields.String,
        'avg':fields.Float

    }

    # 添加电影

    data_fields = {
        'banners': fields.List(fields.Nested(banner_fields)),
        'hot_movies': fields.List(fields.Nested(movie_fields)),
        'ready_movies': fields.List(fields.Nested(movie_fields)),
        'hot_count': fields.Integer,
        'ready_count': fields.Integer
    }

    result_fields = {
        'status': fields.Integer(default=200),
        'msg': fields.String(default='success'),
        'data': fields.Nested(data_fields)
    }


class RatingFields:
    data_fields = {
        'movie_id': fields.Integer,
        'score': fields.Float,
        'name': fields.String,
        'image': fields.String,
    }

    result_fields = {
        'status': fields.Integer(default=200),
        'msg': fields.String(default='success'),
        'data': fields.List(fields.Nested(data_fields))
    }


class AreaFields:

    data_fields = {
        'first':fields.String,
        'short_name':fields.List(fields.String)
    }
    result_fields = {
        'status': fields.Integer(default=200),
        'msg': fields.String(default='success'),
        'data': fields.List(fields.Nested(data_fields))
    }




