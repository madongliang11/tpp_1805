from flask_restful import Api

from apps.cinemas.apis import CinemaResource, CinemasDistrictResource, CinemaDetailResource
from apps.main.apis import IndexResource, HotRankingResource, AreaResource
from apps.movie.apis import MoviesPageResource, MovieDetailResouce
from apps.order.apis import SeatOrderResource

api = Api()


def init_api(app):
    api.init_app(app)


api.add_resource(IndexResource, '/')
api.add_resource(HotRankingResource, '/score/')
api.add_resource(MoviesPageResource,'/movies/')
api.add_resource(AreaResource,'/city')
api.add_resource(CinemaResource,'/cinemas/')
api.add_resource(CinemasDistrictResource, '/cinemas/district/')
# 影院详情
api.add_resource(CinemaDetailResource,'/cinemas/detail/')
api.add_resource(SeatOrderResource,'/seat/')
api.add_resource(MovieDetailResouce,'/movies/detail/')

