# -*- coding: utf-8 -*-

from flask import flash, redirect, url_for, render_template,session,request
from flask import abort
from sayhello import app, db
from sayhello.forms import HelloForm
from sayhello.models import Message
from flask_login import LoginManager, login_required, current_user, login_user, UserMixin, logout_user

# 配置 Flask-Login
app.secret_key = 'your_secret_key'
login_manager = LoginManager(app)
login_manager.login_view = 'login'


# 模拟一个用户
users = [{'id': '1', 'username': 'zyg', 'password': '123'}]

# 定义 User 类
class User(UserMixin):
    def __init__(self, user):
        self.id = user['id']
        self.username = user['username']
        self.password = user['password']

    def get_id(self):
        return self.id

# 用户加载函数
@login_manager.user_loader
def load_user(user_id):
    for user in users:
        if user['id'] == user_id:
            return User(user)
    return None

# 登录视图函数
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        for user in users:
            if user['username'] == username and user['password'] == password:
                user_obj = User(user)
                login_user(user_obj)
                return redirect(url_for('index'))
        return '用户名或密码错误！'
    return render_template('login.html')

# 保护视图函数，只有登录用户才能访问
@app.route('/protected')
@login_required
def protected():
    return '这是需要登录才能访问的页面！'

# 登出视图函数
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return '退出登录成功！'


@app.route('/')
@login_required
def index():
    # class WeatherData:
    #     #温度 湿度	负离子数	风向	风速	大气压	降雨量	噪音	紫外线强度	氧气	时间
    #
    #     def __init__(self, temporary,humidity, ion_count, wind_direction, wind_speed, atmospheric_pressure, rainfall, noise,
    #                  uv_index, oxygen_level, timestamp):
    #         self.temporary=temporary
    #         self.humidity = humidity
    #         self.ion_count = ion_count
    #         self.wind_direction = wind_direction
    #         self.wind_speed = wind_speed
    #         self.atmospheric_pressure = atmospheric_pressure
    #         self.rainfall = rainfall
    #         self.noise = noise
    #         self.uv_index = uv_index
    #         self.oxygen_level = oxygen_level
    #         self.timestamp = timestamp
    # datalist=[
    #     WeatherData(1.2,    90,	944,	0,	0,	871.7,	0,	80.6,	0.06,	20.9,2023-1-1-00-00-00),
    #     WeatherData(1.3,	90,	920,	0,	0,	871.9,	0,	43.5,	0.06,	20.9,2023-1-1-00-00-00)
    # ]

    # 加载所有的记录
    # form = HelloForm()
    # if form.validate_on_submit():
    #     name = form.name.data
    #     body = form.body.data
    #     message = Message(body=body, name=name) # 实例化模型类，创建记录
    #     db.session.add(message) # 添加记录到数据库会话
    #     db.session.commit() # 提交会话
    #     flash('Your message have been sent to the world!')
    #     return redirect(url_for('index'))

    messages = Message.query.order_by(Message.rainfall.desc()).limit(1).all() # 只传前1条数据
    return render_template('index.html', messages=messages)
