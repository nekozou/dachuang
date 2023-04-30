# -*- coding: utf-8 -*-
#自定义flask命令
import click
import csv
import mysql.connector
from sayhello import app, db
from sayhello.models import Message

@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop): # 将本地数据库数据导入项目data.db文件中
    # 保证数据库表结构和模型类同步更新
    if drop:
        click.confirm('This operation will delete the database, do you want to continue?', abort=True)
    db.drop_all()
    click.echo('Drop tables.')
    db.create_all()

    # 连接数据库
    conn = mysql.connector.connect(host='localhost', port=3306, user='root', passwd='', db='DcData')
    # 获取游标
    cursor = conn.cursor()
    # 执行SQL查询
    cursor.execute('SELECT * FROM miyun_raw_nais')
    # 获取结果
    results = cursor.fetchall()
    # 打印结果，测试
    # for row in results:
    #     print(row)
    for row in results:
        message = Message(
            id = str(row[0]),
            record_time = str(row[1]),
            nai = str(row[2])
        )
        db.session.add(message)
    db.session.commit()
    # 关闭连接
    cursor.close()
    conn.close()

    click.echo('Initialized database.') # 提示语句