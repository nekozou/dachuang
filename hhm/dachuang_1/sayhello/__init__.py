# -*- coding: utf-8 -*-

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

# 使用硬编码的形式写出包名称作为程序名称
app = Flask('sayhello')
# 加载配置
app.config.from_pyfile('settings.py')

app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

# 初始化扩展
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

from sayhello import views, errors, commands
