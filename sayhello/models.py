# -*- coding: utf-8 -*-
from datetime import datetime
from sayhello import db
# 建表:id,record_time,nai
class Message(db.Model):
    id = db.Column(db.String, primary_key=True)     # id
    record_time = db.Column(db.String)             # 记录时间
    nai = db.Column(db.String)                      # 负氧离子浓度