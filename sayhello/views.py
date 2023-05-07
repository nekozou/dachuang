# -*- coding: utf-8 -*-
import io
from flask import flash, redirect, url_for, render_template, session, request
from sayhello import app, db
import pandas as pd
from datetime import datetime
from matplotlib import pyplot, pyplot as plt
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sayhello.models import Message
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM


# 算法模型
def model():
    # 连接数据库、查询数据、画图的代码
    results = Message.query.all()
    dates = []
    for c in results:
        date = datetime.strptime(c.record_time, '%Y-%m-%d %H:%M:%S')
        dates.append(datetime.strftime(date, '%Y-%m-%d'))
    nais = [x.nai for x in results]

    # 画原始数据静态图
    def Image(): # 画2021-06-03变化图像
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
        with open('sayhello/static/ImageDay.png', 'wb') as f:
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
        with open('sayhello/static/ImageMon.png', 'wb') as f:
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
        with open('sayhello/static/ImageYear.png', 'wb') as f:
            f.write(img.getvalue())

    # 数据处理
    values = []; sum_tmp = 0; len_tmp = 0
    for i in range(len(dates) - 1): # 剔除有缺失值的某天数据
        if (dates[i] == dates[i + 1]):
            sum_tmp += int(nais[i])
            len_tmp += 1
        else:
            if (len_tmp == 47):
                values.append((int(sum_tmp) + int(nais[i])) // 48)
            sum_tmp = 0; len_tmp = 0

    # 将数据归一化
    data = values
    data = np.array(data)
    data = data.reshape(-1,1)
    data = data / np.max(data)
    # 构建模型
    model = Sequential()
    model.add(LSTM(100, input_shape=(1,1), return_sequences=True))
    model.add(LSTM(100))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    # 训练模型
    model.fit(data, data, epochs=200, verbose=0)
    # 预测并计算损失
    predict = model.predict(data[-10:])
    loss = np.mean((predict - data[-10:]) ** 2)
    print("loss:", loss) # 2.7088473683719024e-07

    # 训练模型并保存图片
    history = model.fit(data, data, epochs=500, verbose=0)
    # 预测数据图
    predict = model.predict(data)
    plt.plot(data, color='blue', label='Actual')
    plt.plot(predict, color='red', label='Predicted')
    plt.title('Prediction vs Actual')
    plt.legend()
    plt.savefig('sayhello/static/预测值-真实值对比.png')
    # 损失值图
    loss = history.history['loss']
    plt.plot(loss)
    plt.title('Loss curve')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.savefig('sayhello/static/损失值.png')
    plt.show()
    return 'Image saved!'

@app.route('/')
def index():
    return render_template('index.html')

