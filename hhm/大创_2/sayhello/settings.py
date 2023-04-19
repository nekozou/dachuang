# -*- coding: utf-8 -*-

import os
import sys

from sayhello import app

# 判断此电脑是哪个系统
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

#确定路径
# os.path.dirname(app.root_path)获取上层目录
# app.root_path属性存储程序实例所在的路径
dev_db = prefix + os.path.join(os.path.dirname(app.root_path), 'data.db') # 将数据库文件放在了项目文件下，通过Flask拓展类自动创建文件

SECRET_KEY = os.getenv('SECRET_KEY', 'secret string')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', dev_db)
