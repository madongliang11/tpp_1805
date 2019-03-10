from flask_cors import CORS
from flask_uploads import UploadSet, IMAGES, DOCUMENTS, configure_uploads
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_caching import Cache


# 初始化第三方插件
def init_ext(app):
    # 初始化数据库
    init_db(app)
    # 初始化登录模块
    init_login(app)
    # 初始化缓存
    init_caching(app)
    # 初始化文件上传
    init_upload(app)
    # 解决跨域请求的问题
    init_cors(app)


db = SQLAlchemy()
migrate = Migrate()


# 初始化数据库
def init_db(app):
    db.init_app(app)
    migrate.init_app(app=app, db=db)


# 实例化登录对象
lm = LoginManager()


def init_login(app: Flask):
    lm.login_view = '/account/login/'
    lm.session_protection = 'strong'
    lm.init_app(app)


# 其他配置
"""
session 存储的位置
# cookie 相关配置
"""

cache = Cache()

"""
pip install redis

CACHE_DEFAULT_TIMEOUT 连接redis超时时间
CACHE_KEY_PREFIX     redis缓存key的前缀
CACHE_REDIS_HOST       ip
CACHE_REDIS_PORT       端口
CACHE_REDIS_PASSWORD   密码
CACHE_REDIS_DB         redis数据库的索引号
CACHE_REDIS_URL        使用url连接地址的方式配置连接数据
"""


def init_caching(app: Flask):
    cache.init_app(app)


"""
文件上传配置
pip install flask-uploads
"""

"""
post请求 form-data

UploadSet 文件上传的核心对象

"""

# media
"""
name 上传文件的子目录 默认是files  
extensions  上传文件的类型(扩展名),默认是 TEXT + DOCUMENTS + IMAGES + DATA
default_dest 配置文件上传的根目录 例如D:\work\PycharmProjects\1805\flask_cache\apps\media
"""
# 上传图片
img_set = UploadSet(name='images', extensions=IMAGES)
# 上传文档文件
doc_set = UploadSet(name='doc', extensions=DOCUMENTS)

"""
 config_uploads 初始化UploadSet对象
"""


def init_upload(app: Flask):
    # 初始化img_set
    configure_uploads(app, img_set)
    configure_uploads(app, doc_set)


# 协议 ip地址, 端口
# 解决前后端分离跨域问题
# cors = CORS(resources={r"/api/*": {"origins": "*"}})
cors = CORS()

def init_cors(app):
    cors.init_app(app)
