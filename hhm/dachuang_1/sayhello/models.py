# -*- coding: utf-8 -*-

#数据库模型
from datetime import datetime

from sayhello import db # 为这个项目使用

# 建表:name,id,body,timestamp
class Message(db.Model):
    # 在这里将数据库的结构改写
    # time1 = db.Column(db.Date, primary_key=True)
    # temp = db.Column(db.Double)
    # humi = db.Column(db.Integer)
    # noin = db.Column(db.Integer)
    # wd = db.Column(db.Integer)
    # ws = db.Column(db.Double)
    # ap = db.Column(db.Double)
    # rainfall = db.Column(db.Double)
    # noise = db.Column(db.Double)
    # ui = db.Column(db.Double)
    # o2 = db.Column(db.Double)
    # id = db.Column(db.Integer, primary_key=True)
    # name = db.Column(db.String(20))
    # body = db.Column(db.String(200))
    # timestamp作为时间戳
    # 默认值为utcnow，可以通过索引寻找
    # timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    time1 = db.Column(db.String, primary_key=True)
    temp = db.Column(db.String)
    humi = db.Column(db.String)
    noin = db.Column(db.String)
    wd = db.Column(db.String)
    ws = db.Column(db.String)
    ap = db.Column(db.String)
    rainfall = db.Column(db.String)
    noise = db.Column(db.String)
    ui = db.Column(db.String)
    o2 = db.Column(db.String)