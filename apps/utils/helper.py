
# 随机生成订单号
import datetime
import random


def product_code():
    date_code = datetime.datetime.now().strftime('%Y%m%d%H%I%S%f')
    random_code = random.randint(1000,9999)
    return f'{date_code}{str(random_code)}'

