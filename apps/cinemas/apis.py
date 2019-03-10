from flask_restful import Resource, reqparse

from apps.cinemas.helper import AreaFields, CinemasFields, CinemasDetauil
from apps.cinemas.models import Cinema, HallScheduling
from apps.main.models import Area
from apps.utils.resp_reslut import to_response_error, to_response_success


class CinemaResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('city',type=str,default='2')
        self.parser.add_argument('district',type=int)
        self.parser.add_argument('sort', type=int)
        self.parser.add_argument('keyword', type=str)
    '''
    区域信息
    影院信息
    '''
    def get(self):
        try:
            args = self.parser.parse_args()
            city = args.get('city')
            # 获取区域信息
            district = args.get('district')
            sort = args.get('sort')
            query = Cinema.query.filter(Cinema.city==city)
            if district and district>0:
                # 如果有 选中区域
                query = query.filter(Cinema.district==district)
            # 1表示升序 2表示降序
            if sort==1:
                # 表示降序
                query = query.order_by(Cinema.score.desc())
            elif sort==2:
                query.order_by(Cinema.score.asc())
            cinemas = query.all()
            return to_response_success(cinemas,fields=CinemasFields.result_fields)
        except Exception as e:
            return to_response_error()



class CinemasDistrictResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('city',type=str,default='北京')
    def get(self):
        try:
            args = self.parser.parse_args()
            city =  args.get('city')
            city = Area.query.filter(Area.short_name==city,Area.level==2).first()
            districts = Area.query.filter(Area.parent_id == city.aid,Area.level==3).all()
            return to_response_success(districts,fields=AreaFields.result_fields)
        except:
            return to_response_error()


'''
查询影院详情
影院表
电影表
排片表
影厅表

1、影院的信息
2、影院排片信息


必要参数影院id

多对多
'''

class CinemaDetailResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('cid',type=int,required=True)
    def get(self):
        try:
            cid = self.parser.parse_args().get('cid')
            # 根据影院id查出该影院下所有影片排片期
            hs_list = HallScheduling.query.filter(HallScheduling.cinema_id==cid).all()
            movies=[]
            for hs in hs_list:
                # 判断影片名是否重复（子表查主表【一对多】）
                if hs.movie not in movies:
                    movies.append(hs.movie)
            data = {
                # 主表Cinema与子表HallScheduling是一对多关系，通过子表查主表，子表对象.(backref对应属性值)
                # 通过主表查子表，主表对象.(主表中relationgship对应的属性字段)
                'cinema':hs_list[0].cinema,
                'movies':movies,
                'movie':hs_list[0].movie,
                'hs_list':hs_list
            }
            return to_response_success(data=data,fields=CinemasDetauil.result_fields)
        except:
            return to_response_error()



class HallSchedulingResource(Resource):
    def get(self):
        pass

    def post(self):
        pass

    def put(self):
        pass


