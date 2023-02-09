# -*- coding: utf-8 -*-

from flask import flash, redirect, url_for, render_template,session,request

from sayhello import app, db
from sayhello.forms import HelloForm
from sayhello.models import Message

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method =='GET':

        return render_template('login.html')
    user=request.form.get('user')
    pwd=request.form.get('password')
    if user=='zyg':
        return redirect(url_for('index'))
    else:
        return('用户名错误')
@app.route('/', methods=['GET', 'POST'])
def index():
    # 先删掉数据库原先内容

    # 加载所有的记录
    form = HelloForm()
    if form.validate_on_submit():
        name = form.name.data
        body = form.body.data
        message = Message(body=body, name=name) # 实例化模型类，创建记录
        db.session.add(message) # 添加记录到数据库会话
        db.session.commit() # 提交会话
        flash('Your message have been sent to the world!')
        return redirect(url_for('index'))

    messages = Message.query.order_by(Message.timestamp.desc()).all()
    return render_template('index.html', form=form, messages=messages)
