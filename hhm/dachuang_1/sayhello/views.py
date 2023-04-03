# -*- coding: utf-8 -*-
from flask import flash, redirect, url_for, render_template,session,request
from flask import abort
from sayhello import app, db
from sayhello.forms import HelloForm
from sayhello.models import Message
from flask_login import LoginManager, login_required, current_user, login_user, UserMixin, logout_user


import pandas as pd
from pandas import read_csv
from pandas import DataFrame
from pandas import concat
from datetime import datetime
from math import sqrt
from numpy import concatenate
from matplotlib import pyplot
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM

# print()不省略输出
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 100)
pd.set_option('display.width', 1000)

# 加载数据
dataset = read_csv('data.csv')
# 打印及保存
# print(dataset.head(5))
dataset.to_csv('pollution.csv')

# 删除时间那一列
dataset = read_csv('pollution.csv', header=0, index_col=0)
dataset.drop('Time', axis=1, inplace=True) # 删除时间那一列
values = dataset.values # 只取值，不取索引

"""
# 画子图
groups = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] # 绘制指定列的图
i = 1
pyplot.figure() # 绘制每一列
for group in groups:
    pyplot.subplot(len(groups), 1, i) # 行数、列数、索引数
    pyplot.plot(values[:, group]) # 取所有行的group列
    pyplot.title(dataset.columns[group], y=0.5, loc='right') # 命名
    i += 1
pyplot.show()
print(dataset.head(5))
"""

# 将数据转为监督学习所需格式
def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
    n_vars = 1 if type(data) is list else data.shape[1]
    df = DataFrame(data)
    cols, names = list(), list()
    # 输入步长序列 (t-n, ... t-1)
    for i in range(n_in, 0, -1):
        cols.append(df.shift(i))
        names += [('var%d(t-%d)' % (j+1, i)) for j in range(n_vars)]

    # 输出（预测）步长序列 (t, t+1, ... t+n)
    for i in range(0, n_out):
        cols.append(df.shift(-i))
        if i == 0:
            names += [('var%d(t)' % (j+1)) for j in range(n_vars)]
        else:
            names += [('var%d(t+%d)' % (j+1, i)) for j in range(n_vars)]

    # 合在一次
    agg = concat(cols, axis=1)
    agg.columns = names
    # 删除有空值的行
    if dropnan:
        agg.dropna(inplace=True)
    return agg

# 确保所有的数都是浮点数
values = values.astype('float32')
# 归一化所有的特征
scaler = MinMaxScaler(feature_range=(0, 1))
scaled = scaler.fit_transform(values)
# 处理数据符合监督学习格式
reframed = series_to_supervised(scaled, 1, 1)
# print(reframed.head(5))
# 删除我们不想预测的列
reframed.drop(reframed.columns[[9,11,12,13,14,15,16,17,18,19]], axis=1, inplace=True)
# print(reframed.head())

# 划分数据集
values = reframed.values
n_train_hours = 800 # 拿800作为训练数据集，随便定的，大概比例是50%
train = values[:n_train_hours, :]
test = values[n_train_hours:,   :]
# 拆分为输入和输出
train_X, train_y = train[:, :-1], train[:, -1]
test_X, test_y = test[:, :-1], test[:, -1]
# 将输入重塑为3维向量格式将[样本、时间步长、特征]
train_X = train_X.reshape((train_X.shape[0], 1, train_X.shape[1]))
test_X = test_X.reshape((test_X.shape[0], 1, test_X.shape[1]))
# print(train_X.shape, train_y.shape, test_X.shape, test_y.shape)

train_loss = [] # 存储损失的数值，传给前端
test_loss = []

# 设计神经网络
model = Sequential()
model.add(LSTM(50, input_shape=(train_X.shape[1], train_X.shape[2]))) # 训练50次
model.add(Dense(1))
model.compile(loss='mae', optimizer='adam')

# 使用训练集及测试集进行集合
history = model.fit(train_X, train_y, epochs=50, batch_size=72, validation_data=(test_X, test_y), verbose=2, shuffle=False)
pyplot.plot(history.history['loss'], label='train') # 损失值作为y轴
train_loss.append(history.history['loss'])
pyplot.plot(history.history['val_loss'], label='test')
test_loss.append(history.history['loss'])
pyplot.legend()
pyplot.show()

# 进行预测
print('--------------------------------------------------')
yhat = model.predict(test_X)
test_X = test_X.reshape((test_X.shape[0], test_X.shape[2]))
# 反比例预测 将预测与测试数据集结合起来并反转缩放比例
inv_yhat = concatenate((yhat, test_X[:, -9:]), axis=1)
inv_yhat = scaler.inverse_transform(inv_yhat)
inv_yhat = inv_yhat[:,0]
# 实际的反转比例
test_y = test_y.reshape((len(test_y), 1))
inv_y = concatenate((test_y, test_X[:, -9:]), axis=1)
inv_y = scaler.inverse_transform(inv_y)
inv_y = inv_y[:,0]
# 计算均方根误差
rmse = sqrt(mean_squared_error(inv_y, inv_yhat))
print('Test RMSE: %.3f' % rmse) # 最终结果



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

    # messages = Message.query.order_by(Message.rainfall.desc()).limit(1).all() # 只传前1条数据
    return render_template('index.html', train_loss = train_loss, test_loss = test_loss)
