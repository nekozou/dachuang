# -*- coding: utf-8 -*-
# from datetime import datetime
from sayhello import db # 为这个项目使用

# 建表:name,id,body,timestamp
class Message(db.Model):
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