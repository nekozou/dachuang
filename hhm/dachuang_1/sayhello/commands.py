# -*- coding: utf-8 -*-
#自定义flask命令
import click
import csv

from sayhello import app, db
from sayhello.models import Message

#删除表后重建
@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop): # 若有数据库则删除，然后重新给项目创建一个数据库
    """Initialize the database."""
    if drop:
        click.confirm('This operation will delete the database, do you want to continue?', abort=True)
        db.drop_all()
        click.echo('Drop tables.')
    db.create_all()
    click.echo('Initialized database.')

# 生成虚拟数据
# @app.cli.command()
# @click.option('--count', default=20, help='Quantity of messages, default is 20.')
# def forge(count):
#     """Generate fake messages."""
#     from faker import Faker
#
#     db.drop_all()
#     db.create_all()
#
#     fake = Faker('zh_CN')
#     click.echo('Working...')
#
#     for i in range(count):
#         message = Message(
#             name=fake.name(),
#             body=fake.sentence(),
#             timestamp=fake.date_time_this_year()
#         )
#         db.session.add(message)
#
#     db.session.commit()
#     click.echo('Created %d fake messages.' % count)

# 给项目数据库data.db导入数据库
@app.cli.command()
@click.option('--count', default=20, help='Quantity of messages, default is 20.')
def ImportData(count):

    # 若有数据库则删除，然后新建一个项目数据库
    db.drop_all()
    db.create_all()

    click.echo('导入数据中...')

    with open('data.csv', 'r') as file:
        reader = csv.reader(file)

        # 读取头部并去掉空格
        headers = [header.strip() for header in next(reader)]
        for row in reader:
            row_data = {}
            for i, value in enumerate(row):
                row_data[headers[i]] = value
            message = Message(
                time1 = row_data['Time'],
                temp = row_data['Temp'],
                humi = row_data['Humi'],
                noin = row_data['Noin'],
                wd = row_data['Wd'],
                ws = row_data['Ws'],
                ap = row_data['Ap'],
                rainfall = row_data['Rainfall'],
                noise = row_data['Noise'],
                ui = row_data['Ul'], # 这里字母有些问题
                o2 = row_data['O2']
            )
            db.session.add(message)

        db.session.commit()
    # for i in range(count):
    #     message = Message(
    #         name=fake.name(),
    #         body=fake.sentence(),
    #         timestamp=fake.date_time_this_year()
    #     )
    #     db.session.add(message)
    #
    # db.session.commit()
    click.echo('\n导入数据成功')