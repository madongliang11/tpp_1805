from flask_restful import Resource, reqparse
from sqlalchemy import func, desc

from apps.ext import cache
from apps.main.field import RatingFields, IndexFields, AreaFields
from apps.main.models import Banner, Movie, Rating, Area
from apps.utils.resp_reslut import to_response_success, to_response_error

"""

"""

# limit  offset
'''
横向拆分 经常变化的数据尽量拆分
经常修改的字段会开事物
缓存
读写分离 主从赋值


'''

class IndexResource(Resource):
    def get(self):
        # 查询轮播的相关信息
        #
        # SELECT  *  FROM MOVIE LIMIT 0,5
        # SELECT  * FROM   LIMIT 10  OFFSET 1
        # (page-1)*size
        try:
            banners = Banner.query.filter(Banner.is_delete is False).order_by(Banner.order.desc()).all()
            hot_movies = Movie.query.filter(Movie.flag == 1).order_by(Movie.open_day).limit(5).offset(0).all()
            # 给正在上映的电影绑定评分
            for hot_movie in hot_movies:
                avgtuple = Rating.query.with_entities(func.round(func.avg(Rating.score),1))\
                    .join(Movie,hot_movie.id==Rating.movie_id).group_by(Rating.movie_id).first()
                if avgtuple:
                    hot_movie.avg=avgtuple[0]
            ready_movies = Movie.query.filter(Movie.flag == 2).order_by(Movie.open_day).limit(5).offset(0).all()
            hot_count = Movie.query.filter(Movie.flag == 1).count()
            ready_count = Movie.query.filter(Movie.flag == 2).count()
            data={
                'banners': banners,
                'hot_movies': hot_movies,
                'ready_movies': ready_movies,
                'hot_count': hot_count,
                'ready_count': ready_count
            }
            return to_response_success(data=data, fields=IndexFields.result_fields)
        except Exception as e:
            return to_response_error()


'''
分组查询 group_by
分组统计 func.max()  func.count()  func.avg()
排序  直接通过字段可以调desc() 如果涉及分组函数，需要通过别名排序，
即desc(别名)  创建别名可以通过 label（别名）
'''

# 票房排行接口
class HotRankingResource(Resource):
    def get(self):
        # label 给分组函数起别名
        # select AVG(score) avg from rating
        # group by movie_id
        # order by avg desc
        # 分组 统计group_by(分组字段，..)
        # try:
        #     # [()]
        #     ranking_moviess = Rating.query.with_entities(Rating.movie_id, func.avg(Rating.score).label('avg')) \
        #         .group_by(Rating.movie_id).order_by(desc('avg')).limit(5).all()
        #     data = []
        #     for rank in ranking_moviess:
        #         data.append({'score': rank[1]})
        #     return to_response_success(data=data, fields=RatingFields.result_fields)
        # except Exception as e:
        #     return to_response_error()
        '''
        多表查询
        1、确定表
            rating表    评分
            movie表     电影id
        2、确定关联字段
            id = movie_id
        select m.show_name,m.id,m.image,round(AVG(r.score)) avg
        from movie m, rating r
        where m.id = r.movie_id
        group by r.movie_id
        order by avg desc
        '''
        try:
            ratings = Rating.query.with_entities(Rating.movie_id,func.round(func.avg(Rating.score),1).label('sorce'),
                                       Movie.image,Movie.show_name).join(Movie,Movie.id==Rating.movie_id)\
                .group_by(Rating.movie_id).order_by(desc('sorce')).limit(5).all()
            data = [{'movie_id':rating[0],
                     'score':rating[1],
                     'image':rating[2],
                     'name':rating[3]}
                    for rating in ratings]
            return to_response_success(data=data, fields=RatingFields.result_fields)
        except:
            return to_response_error()
        # try:
        #     keys = ['movie_id', 'score', 'show_name', 'image']
        #     score = Rating.query.with_entities(Rating.movie_id, func.avg(Rating.score).label('avg')).group_by(
        #         Rating.movie_id).order_by(desc('avg')).limit(5).all()
        #     data_list = Rating.query.with_entities(Rating.movie_id, func.avg(Rating.score).label('avg'),
        #                                            Movie.show_name,
        #                                            Movie.image).join(Movie, Movie.id == Rating.movie_id).group_by(
        #         Rating.movie_id).order_by(desc('avg')).limit(5).all()
        #     # data = db.session.query(Rating.movie_id, func.avg(Rating.score).label('avg'), Movie.image,Movie.show_name).join(Movie, Movie.id == Rating.movie_id).group_by(Rating.movie_id).order_by(desc('avg')).limit(5).all()
        #     data = [dict(zip(keys, d)) for d in data_list]
        #     return to_response_success(data=data, fields=RatingFields.result_fields)
        # except Exception as e:
        #     return to_response_error()

# 给电影添加评分的接口


class AreaResource(Resource):
    @cache.cached(10*24*60)
    def get(self):
        li = [chr(i) for i in range(ord("A"), ord("Z") + 1)]
        data = []
        for i in li:
            # [(城市),(城市),()...]
            cities = Area.query.with_entities(Area.short_name).filter(Area.level==2,Area.first==i).order_by(Area.first.asc()).all()
            city_list = []
            # 转换成[城市,城市,...]
            for city in cities:
                city_list += list(city)
            # 合成[{'first':A,'short_name':[城市,城市..]},{},{}..]
            data.append({'first':i,'short_name':city_list})
        # 第二种
        # firsts = Area.query.with_entities(Area.first).group_by(Area.first).order_by(Area.first).all()
        # areas = []
        # for first in firsts:
        #     areas.append({'first':first[0],'short_name':Area.query.filter(Area.first==first[0],Area.level==2).all()})
        return to_response_success(data=data, fields=AreaFields.result_fields)





