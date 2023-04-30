# -*- coding: utf-8 -*-
import io

from flask import flash, redirect, url_for, render_template, session, request
from sayhello import app, db
from flask_login import LoginManager, login_required, current_user, login_user, UserMixin, logout_user
import pandas as pd
from pandas import read_csv

from pandas import DataFrame
from pandas import concat
from datetime import datetime
from math import sqrt
from numpy import concatenate
from matplotlib import pyplot, pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sayhello.forms import HelloForm
from sayhello.models import Message
from flask import abort

# print()不省略输出
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 100)
pd.set_option('display.width', 1000)





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


# @app.route('/')
# @login_required
# def index():
#     df = pd.read_csv('data.csv')
#     data = df.to_dict(orient='records')
#     #return render_template('index.html', train_loss=train_loss, test_loss=test_loss)
#     return render_template('index.html',data=data)

# 测试
@app.route('/')
def index():
    # 连接数据库、查询数据、画图的代码
    results = Message.query.all()
    dates = []
    for c in results:
        date = datetime.strptime(c.record_time, '%Y-%m-%d %H:%M:%S')
        dates.append(datetime.strftime(date, '%Y-%m-%d'))
    nais = [x.nai for x in results]

    # 画2021-06-03变化图像
    dates_day = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5,
                 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0, 10.5, 11.0, 11.5, 12.0, 12.5, 13.0,
                 13.5, 14.0, 14.5, 15.0, 15.5, 16.0, 16.5, 17.0, 17.5, 18.0, 18.5, 19.0,
                 19.5, 20.0, 20.5, 21.0, 21.5, 22.0, 22.5, 23.0, 23.5]
    nais_day = nais[269:317] # 270-317
    plt.figure(figsize=(15, 7))
    plt.plot(dates_day, nais_day)
    plt.title('Daily Cycle of Nai')
    plt.xlabel('Time')
    plt.ylabel('Nai')
    plt.grid(True)
    img = io.BytesIO()
    plt.savefig(img, format='png')
    with open('ImageDay.png', 'wb') as f:
        f.write(img.getvalue())

    # 画2021-06月的图片
    dates_mon = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17,
                 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
    nais_mon = []
    nais_tmp_mon = nais[191:1610] # 192-1610
    dates_tmp_mon = dates[191:1610]
    index_mon = "2021-06"
    for i in range(1, 31):
        index = ""
        if (i < 10):
            index = index_mon + "-0" + str(i)
        else:
            index = index_mon + "-" + str(i)
        sum = 0
        len_tmp = 0
        for j in range(len(dates_tmp_mon)):
            if (index == dates_tmp_mon[j]):
                sum += int(nais_tmp_mon[j])
                len_tmp += 1
        if len_tmp > 0:
            nais_mon.append(sum // len_tmp)
        else:
            nais_mon.append(0)  # 如果len_tmp为0,那么nais_mon加入0值

    plt.figure(figsize=(15, 7))
    plt.plot(dates_mon, nais_mon)
    plt.title('Monthly Cycle of Nai')
    plt.xlabel('Time')
    plt.ylabel('Nai')
    plt.grid(True)
    img = io.BytesIO()
    plt.savefig(img, format='png')
    with open('ImageMon.png', 'wb') as f:
        f.write(img.getvalue())

    # 画2022年的图片
    dates_year = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    nais_year = []
    nais_tmp_year = nais[10298:26744] #  10299-26744
    dates_tmp_year = dates[10298:26744]
    index_year = "2022-"
    for i in range(1, 13):
        index = ""
        if (i < 10):
            index = index_year + "0" + str(i)
        else:
            index = index_year + str(i)
        sum = 0
        len_tmp = 0
        print("index:", index)
        for j in range(len(dates_tmp_year)):
            str_tmp = dates_tmp_year[j][:7]
            if (str_tmp == "2022-11"):
                print(nais_tmp_year[j])
            if (index == str_tmp):
                sum += int(nais_tmp_year[j])
                len_tmp += 1
        print("sum:", sum)
        print("len_tmp", len_tmp)
        if len_tmp > 0:
            nais_year.append(sum // len_tmp)
        else:
            nais_year.append(0)  # 如果len_tmp为0,那么nais_mon加入0值

    plt.figure(figsize=(15, 7))
    plt.plot(dates_year, nais_year)
    print(dates_year)
    print(nais_year)
    plt.title('Annual Cycle of Nai')
    plt.xlabel('Time')
    plt.ylabel('Nai')
    plt.grid(True)
    img = io.BytesIO()
    plt.savefig(img, format='png')
    with open('ImageYear.png', 'wb') as f:
        f.write(img.getvalue())

    # 模型
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

    return 'Image saved!'