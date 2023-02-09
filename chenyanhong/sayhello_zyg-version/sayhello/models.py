# -*- coding: utf-8 -*-

#数据库模型
from datetime import datetime

from sayhello import db

# 建表:name,id,body,timestamp
class Message(db.Model):
    # id作为主键
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    body = db.Column(db.String(200))
    # timestamp作为时间戳
    # 默认值为utcnow，可以通过索引寻找
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
