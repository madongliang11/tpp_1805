# 响应成功的数据
#
from flask_restful import marshal, fields


def to_response_success(data, status=200, msg='成功', fields=None):
    result = {
        'status': status,
        'msg': msg,
        'data': data
    }
    return marshal(result, fields)


error_result_fields = {
    'status': fields.Integer(default=404),
    'msg': fields.String(default='失败'),
}


def to_response_error(status=404, msg='失败'):
    result = {
        'status': status,
        'msg': msg,
    }
    return marshal(result, error_result_fields)
