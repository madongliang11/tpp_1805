from flask import Flask
from flask_cors import CORS

from apps.config import DeveloperConfig, ProductConfig, environment
from apps.ext import init_ext
from apps.urls import init_api


def create_app(env_name):
    app = Flask(__name__)
    #  从对象中加载默认的配置文件
    app.config.from_object(environment.get(env_name))
    init_api(app)
    init_ext(app)
    return app
