from flask_restful import Resource, reqparse

from apps.cinemas.models import SeatScheduling, HallScheduling, Seats
from apps.ext import db
from apps.order.helper import SeatOrder
from apps.order.models import Order
from apps.utils.helper import product_code
from apps.utils.resp_reslut import to_response_success, to_response_error


# 选座购票接口
class SeatOrderResource(Resource):
    # 获取排片影片的座位信息
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('hsid',type=int,required=True)
    def get(self):
        try:
            hsid = self.parser.parse_args().get('hsid')
            # ss_list = SeatScheduling.query.filter(SeatScheduling.hs_id==hs_id,SeatScheduling.is_delete==False)
            hs = HallScheduling.query.get(hsid)
            data = {
                'seats':[ss.seat for ss in hs.ss_list],
                'movie':hs.movie,
                'hall':hs.hall,
            }
            return to_response_success(data=data, fields=SeatOrder.result_fields)
        except:
            return  to_response_error()


    # 排座接口
    def post(self):

        return ''

    # 更新座位排期
    def put(self):
        pass

    # 删除
    def delete(self):
        pass


# 订单接口
class OrderResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('uid',type=int,required= True)
        self.parser.add_argument('movie_id', type=int, required=True)
        self.parser.add_argument('hs_id', type=int, required=True)
        # 一键多值
        self.parser.add_argument('seats_ids', type=int, required=True,action='append')
        self.parser.add_argument('ss_id', type=int, required=True,default=1)
    def post(self):
        uid = self.parser.parse_args().get('uid')
        movie_id = self.parser.parse_args().get('movie_id')
        hs_id = self.parser.parse_args().get('hs_id')
        seats_ids = self.parser.parse_args().get('seats_ids')


        # 生成订单号
        # 开启事物
        try:
            db.session.begin()
            # 查询选的座位是否可以购买
            seats = Seats.query.filter(Seats.sid.in_(seats_ids)).all()
            if is_choose(seats):
                # 如果可选，就修改is_choose为false
                for seat in seats:
                    seat.is_choose = False
                db.session.add_all(seats)

                # 订单号
                no = product_code()

                # 计算总金额
                hs = HallScheduling.query.get(hs_id)
                total = hs.current_price * 2
                # 生成订单
                order = Order(no=no,number=2,total=total,)
                # 保存订单
                db.session.add(order)
                db.session.commit()
            else:
                return to_response_error(status=-1,msg='座位已被选')
        except:
            db.session.rollback()

#判断是否可以购买
def is_choose(seats):
    for seat in seats:
        if seat.is_choose:
            continue
        else:
            return False
    return True

