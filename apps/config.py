"""
数据配置
缓存配置
登录配置
文件上传配置



"""
import datetime
import os

BASE_DIR = os.path.dirname(__file__)
UPLOAD_ROOT_PATH = os.path.join(BASE_DIR, 'static/upload/')


class BaseConfig:
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # === 文件上传相关配置====
    # 配置文件上传的根目录
    UPLOADS_DEFAULT_DEST = UPLOAD_ROOT_PATH
    # 生成访问图片的路径
    UPLOADS_DEFAULT_URL = '/static/upload/'
    CACHE_TYPE = 'redis'
    #    配置session的存储方式
    SESSION_TYPE = 'redis'
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=1)
    #     COOKIE
    REMEMBER_COOKIE_NAME = 'session_id'
    # 上传文件的最大长度
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024


def get_db_uri(database: dict):
    engine = database.get('ENGINE') or 'mysql'
    user = database.get('USER') or 'root'
    password = database.get('PASSWORD') or 'root'
    driver = database.get('DRIVER') or 'pymysql'
    host = database.get('HOST') or '127.0.0.1'
    port = database.get('PORT') or '3306'
    name = database.get('NAME')
    charset = database.get('CHARSET') or 'utf8'
    return f"{engine}+{driver}://{user}:{password}@{host}:{port}/{name}?charset={charset}"


# 开发环境
class DeveloperConfig(BaseConfig):
    DEBUG = True
    SECRET_KEY = '123456'
    database = {
        'ENGINE': 'mysql',
        'NAME': 'tpp',
    }
    # 输出sql语句
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = get_db_uri(database)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 缓存配置
    CACHE_REDIS_HOST = '127.0.0.1'
    CACHE_REDIS_PORT = 6379
    # CACHE_REDIS_PASSWORD = ''
    CACHE_REDIS_DB = 1


# 生成数据连接 dialect+driver://username:password@host:port/database

# 生产环境
class ProductConfig(BaseConfig):
    DEBUG = False
    SECRET_KEY = '4ce01aa944434ff4880b29b0992ee846'
    database = {
        'ENGINE': 'mysql',
        'HOST': '112.74.42.138',
        'PORT': '3306',
        'NAME': 'film',
    }
    # 生成环境小设置连接池的数量
    SQLALCHEMY_POOL_SIZE = 100
    # 配置数据连接路径
    SQLALCHEMY_DATABASE_URI = get_db_uri(database)
    # 禁用改动发送信号
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #   缓存配置
    CACHE_REDIS_HOST = '127.0.0.1'
    CACHE_REDIS_PORT = 6379
    # CACHE_REDIS_PASSWORD = ''
    CACHE_REDIS_DB = 1


# 开发环境
ENVI_DEFAULT_KEY = ENVI_DEV_KEY = 'default'
ENVI_PRODUCT_DEFAULT_KEY = 'product'

environment = {
    'default': DeveloperConfig,
    'dev': DeveloperConfig,
    'product': ProductConfig
}

