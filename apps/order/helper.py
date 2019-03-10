from flask_restful import fields


class SeatOrder:
    movie_fields = {
        'id': fields.Integer,
        'show_name': fields.String,
        'type': fields.String,
        'country': fields.String,
        'language': fields.String,
        'duration': fields.Integer,
        'image': fields.String,
    }
    seat_fields = {
        'x':fields.Integer,
        'y':fields.Integer,
        'is_choose':fields.Boolean
    }
    cinema_fields = {
        'cid':fields.Integer,
        'name':fields.String
    }
    hall_fields = {
        'hid':fields.Integer,
        'name':fields.String,
        'cinema':fields.Nested(cinema_fields)
    }
    # 什么时候用fields.List
    data_fields = {
        'seats':fields.List(fields.Nested(seat_fields)),
        'movie':fields.Nested(movie_fields),
        'hall':fields.Nested(hall_fields)
    }
    result_fields = {
        'status': fields.Integer,
        'msg': fields.String,
        'data': fields.Nested(data_fields)
    }


result_files={

}