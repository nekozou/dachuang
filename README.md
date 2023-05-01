[toc]

### 项目运行

1、保证`Python`环境在3.6以上或更高版本（3.6之前可能不支持`pipenv`）。

2、（Windows）`PATH`环境变量包含`Python`可执行文件目录。

3、`pip install pipenv`：安装`pipenv`，后续通过`pipenv`工具来进行依赖管理（也可以使用`pip + virtualenv`）；其中Linux或者macOS系统最好使用`sudo pip install pipenv`命令进行全局安装。

4、`pipenv install`：通过pipenv工具安装`requirements.txt`文件中的依赖。如果之前已经运行过该命令，可以使用`pipenv install --dev`命令只安装开发相关依赖。

5、`pipenv shell`：显式激活虚拟环境。

6、在激活的虚拟环境中，使用`pipenv install flask`命令安装`Flask`框架。

**注：**在Pycharm等IDE中，使用`pipenv --venv`命令查看项目对应的虚拟环境路径，再将解释器路径设置为对应的虚拟环境路径，通常macOS中路径类似`~/.local/share/virtualenvs/helloflaskkSN7ec1K/bin/python`；Windows中路径类似：`C：\Users\Administrator\.virtualenvs\helloflask-5Pa0ZfZw\Scripts\python.exe`。

7、`cd sayhello/`，然后执行`flask run`即可。（若无数据，可先执行`flask importdata`命令，再执行`flask run`）。

配置文件`Pipfile`或`requirements.txt`内容如下：

```php
bootstrap-flask==1.2.0
click==7.1.1
flask-moment==0.9.0
flask-sqlalchemy==2.4.1
flask-wtf==0.14.3
flask==1.1.2
itsdangerous==1.1.0
jinja2==2.11.1
markupsafe==1.1.1
python-dotenv==0.12.0
sqlalchemy==1.3.15
werkzeug==1.0.1
wtforms==2.2.1
# dev
faker==4.0.2
pathtools==0.1.2
python-dateutil==2.8.1
six==1.14.0
text-unidecode==1.3
watchdog==0.10.2
```

---

### 登录

可以在后台`view.py`文件中修改账号密码。

* 账号：`zyg`
* 密码：`123`

---

### 数据

##### 数据库

使用ORM（Object Relational Mapping 对象关系映射）技术，将SQL中的数据表、数据行、字段映射为类、对象和属性。

在本项目中，利用Flask框架中的Flask-SQLAlchemy拓展来完成转换。项目定义类如下：

```py
class Message(db.Model):
    id = db.Column(db.String, primary_key=True)     # id
    recordTime = db.Column(db.String)               # 记录时间
    nai = db.Column(db.String)                      # 负氧离子浓度
```

从数据库文件data.db中查询数据遵从格式：`<模型类>.query.<过滤方法>.<查询方法>`。下面是一些常用的SQLAlchemy查询方法：

```py
get(ident)	# 传入主键值作为参数，返回指定主键值的记录
count()		# 返回查询结果的数量
```

##### 数据预处理

经过检查，有三个数据明显不合理，将其作删除处理，示例如下：

![image](https://user-images.githubusercontent.com/88172940/235351505-3cf7c4a3-dd8f-45a0-818d-c0967169c0a1.png)

---

### 负氧离子浓度

负氧离子浓度在一天中呈周期性变化，粗略原因如下：

上午呈上升趋势（7-10）：

* 植物光合作用旺盛,释放大量负氧离子。植物在光照强、温度适宜的条件下,光合作用最活跃,产生最多的负氧离子。

夜晚呈下降趋势（24-5）：

* 污染物积聚，难以产生大量负氧离子。
* 植物光合作用弱，难以产生大量负氧离子。

---

### 前端展示

##### 展示某一天

从某个范围内随机挑选出某一天的负氧离子数据（展示样例为2021-06-03）进行展示，图像效果如下：

![image](https://user-images.githubusercontent.com/88172940/235342031-f4a937d0-6b51-45e1-9df8-daae0f230615.png)

##### 展示某一个月

从某个范围内随机挑选出某一月的负氧离子数据（展示样例为2021-06）进行展示，并且取负氧离子浓度平均值作为某一天的数据，图像效果如下：

![image](https://user-images.githubusercontent.com/88172940/235343913-493a7a58-61ad-4fa2-a14b-5231b5ee50a0.png)

查看原始数据，峰值匹配成功：

![image](https://user-images.githubusercontent.com/88172940/235343979-0d872d32-9337-4375-ae84-1164c5312006.png)

##### 展示某一年

从某个范围内随机挑选出某一年的负氧离子数据（展示样例为2022年）进行展示，并且取负氧离子浓度平均值作为某一天的数据，图像效果如下：

![image](https://user-images.githubusercontent.com/88172940/235351723-6ccab384-d66e-4b93-851b-90888ce019f4.png)

---

### 算法模型

##### 数据处理

以每天负氧离子平均值作为序列的一个点，注意，若一天中观测点不足48个，则视为无效数据舍去。

##### 结果部分

**预测值与真实值对比图（已归一化处理）：**

![image](https://user-images.githubusercontent.com/88172940/235405654-917a1e98-4f0f-406d-9f30-9a21129caabe.png)

**损失值图：**

![image](https://user-images.githubusercontent.com/88172940/235405618-309a2159-6cf2-4b92-82a0-cf537337934f.png)

##### 模型代码

```py
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
print("loss:", loss)

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
```

