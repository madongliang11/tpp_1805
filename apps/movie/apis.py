from flask_restful import Resource, reqparse
from sqlalchemy import func

from apps.cinemas.models import Cinema

from apps.main.models import Movie, Area, Rating
from apps.movie.field import MoviesFields, MovieDetailFields
from apps.utils.resp_reslut import to_response_success, to_response_error


class MoviesPageResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('page', type=int, default=1)
        self.parser.add_argument('size', type=int, default=10)
        self.parser.add_argument('flag',type=int, default=1)
    def get(self):
        args = self.parser.parse_args()
        page = args.get('page')
        size = args.get('size')
        flag = args.get('flag')
        pagination = Movie.query.filter(Movie.flag==flag).paginate(page=page,per_page=size,error_out=False)
        data = {
            'movies':pagination.items,
            'pagination':pagination,
        }
        return to_response_success(data=data,fields=MoviesFields.result_fields)



class MovieDetailResouce(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('aid',type=int,default=1988)
        self.parser.add_argument('dist_id',type=int)
        self.parser.add_argument('mid',type=int,required=True)
    def get(self):
        try:
            aid = self.parser.parse_args().get('aid')
            movie_id = self.parser.parse_args().get('mid')
            dist_id = self.parser.parse_args().get('dist_id')
            # 通过城市id查寻该城市下地区信息
            areas = Area.query.filter(Area.parent_id == aid,Area.level==3).all()
            # 如果传入城市的地区id，则显示出该城市下地区的影院信息
            # 如果不传，则默显示整个城市下的影院信息
            if dist_id:
                cinemas = Cinema.query.filter(Cinema.city==str(aid),Cinema.district==str(dist_id)).all()
            else:
                cinemas = Cinema.query.filter(Cinema.city==str(aid)).all()
            movie = Movie.query.filter(Movie.id==movie_id).first()
            # 绑定评分
            avgtuple = Rating.query.with_entities(func.round(func.avg(Rating.score), 1)) \
                .join(Movie, movie.id == Rating.movie_id).group_by(Rating.movie_id).first()
            if avgtuple:
                movie.avg = avgtuple[0]
            data = {
                'movie':movie,
                'area':areas,
                'cinema':cinemas,
                'hall': movie.hs_list[0],
                'hallschedul':movie.hs_list,
            }
            return to_response_success(data=data,fields=MovieDetailFields.result_fields)
        except Exception as e:
            print(e)
            return to_response_error()