[toc]

## 前置知识

### 1. 创建项目及初始设置

Ubuntu20.04环境，python版本为3.8。

提前安装：`sudo pip install pipenv`

```shell
mkdir FlaskProject
cd FlaskProject
pipenv install

# 使用pipenv shell 命令激活虚拟环境

# 为每个虚拟环境安装Flask
pipenv install flask
```

`FLASK_ENV`：设置程序运行环境，开发或者调试，`$ export FLASK_ENV=development `

`FLASK_APP`：设置Flask框架需要启动的程序，例如`$ export FLASK_APP=hello.py`

安装用来自动导入系统环境变量的 python-dotenv：

```shell
pip install python-dotenv
vim .env .flaskenv. # flaskenv 用来存储 Flask 命令行系统相关的公开环境变量；而 .env 则用来存储敏感数据
# .flaskenv 文件
FLASK_ENV=development
```

依照书中来给Pycharm设置虚拟环境解释器，其中使用`pipenv --venv`查看项目对应虚拟环境路径。

### 2. 跑通第一个视图函数

/home/hhm/Code/Python/FlaskProject/domes/hello/app.py：

```py
from flask import Flask # 从flask包中引入Flask类
app = Flask(__name__) # 创建实例，根据所处模块赋予__name__变量不同的值

@app.route('/') # 路由装饰器
def index():
    return '<h1>Hello Flask!</h1>'
```

```shell
(FlaskProject)  hhm@hhmm  ~/Code/Python/FlaskProject/domes/hello  flask run
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

![image](https://user-images.githubusercontent.com/88172940/217547669-c19a183a-56d5-4457-806f-d7ad4a2093c5.png)

**动态URL**

```py
![image](https://user-images.githubusercontent.com/88172940/217724711-c6ce180c-e576-4603-8612-dce172edeeb5.png)@app.route('/greet/<name>')
def greet(name):
    return '<h1>Hello, %s!</h1>' % name
```

**url_for()函数**

如果都使用Flask框架提供的url_for()函数来生成url，当一个路由规则被修改时，会自动修改所有相关url。

```py]
from flask import Flask # 从flask包中引入Flask类
app = Flask(__name__) # 创建实例，根据所处模块赋予__name__变量不同的值

@app.route('/') # 路由装饰器
def index():
    return '<h1>Hello Flask!</h1>'
```

最好形式为url_for('index')，调用url_for（'index'）即可获取对应的URL，即“/”。其中index称之为端点，用来标识一个视图函数以及对应的URL规则。

对于带有动态部分的URL：

```py
@app.route('/hello/<name>')
def say_hello(name):
	return 'Hello %s!' % name
```

则使用url_for（'say_hello'，name='Jack'）得到的URL为“/hello/Jack”。

**路由表**

使用`flask routes`可以看到每个路由对应的端点。

**监听**

```py
@app.route('/hello', methods=['GET', 'POST']) # 限定请求方法
def hello():
return '<h1>Hello, Flask!</h1>'
```

405错误响应（Method Not Allowed，表示请求方法不允许）。

**重定向功能**

```py
from flask import Flask, redirect
# ...
@app.route('/hello')
def hello():
return redirect('http://www.example.com')
```

### 3. Ajax

AJAX指异步Javascript和XML（Asynchronous JavaScript And 让
我们可以在不重载页面的情况下和服务器进行数据交换。加上JavaScript和DOM（Document Object Model，文档对象模型），我们就可以在接收到响应数据后局部更新页面。XML），它不是编程语言或通信协议，而是一系列技术的组合体。

### 4. HTTP服务器端推送

在某些场景下，我们需要的通信模式是服务器端的主动推送（server push）。比如，一个聊天室有很多个用户，当某个用户发送消息后，服务器接收到这个请求，然后把消息推送给聊天室的所有用户。

![image](https://user-images.githubusercontent.com/88172940/217688513-c25be003-dfa7-4b2f-ba78-99b2f7eb27e8.png)

### 5. Jinjia2模板引擎

demos/template/watchlist.html

```jinja2
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>{{ user.username }}'s Watchlist</title>
</head>
<body>
<a href="{{ url_for('index') }}">&larr; Return</a>
<h2>{{ user.username }}</h2>{% if user.bio %}
	<i>{{ user.bio }}</i>
{% else %}
	<i>This user has not provided a bio.</i>
{% endif %}
{# 下面是电影清单（这是注释） #}
<h5>{{ user.username }}'s Watchlist ({{ movies|length }}):</h5>
<ul>
	{% for movie in movies %}
		<li>{{ movie.name }} - {{ movie.year }}</li>
	{% endfor %}
</ul>
</body>
</html>
```

**语句：**`{{ % ... % }}`

**表达式：**`{{ ... }}`

**注释：**`{# ... # }`

渲染一个模板，就是执行模板中的代码，并传入所有在模板中使用的变量，渲染后的结果就是我们要返回给客户端的HTML响应。在视图函数中渲染模板时，我们并不直接使用Jinja2提供的函数，而是使用
Flask提供的渲染函数render_template（）。

template/app.py：

```py
user = {
    'username': 'Grey Li',
    'bio': 'A boy who loves movies and music.',
}
movies = [
    {'name':
    {'name':
    {'name':
    {'name':
    {'name':
    {'name':
    {'name':
    {'name':
    {'name':
    {'name':
]
from flask import Flask, render_template
...
@app.route('/watchlist')
def watchlist():
	return render_template('watchlist.html', user=user, movies=movies)
```

### 6. 表单

**html表单**示例如下：

```html
<form method="post">
    <label for="username">Username</label><br>
    <input type="text" name="username" placeholder="Héctor Rivera"><br>
    <label for="password">Password</label><br>
    <input type="password" name="password" placeholder="19001130"><br>
    <input id="remember" name="remember" type="checkbox" checked>
    <label for="remember"><small>Remember me</small></label><br>
    <input type="submit" name="submit" value="Log in">
</form>
```

一般不会在模板中直接使用HTML编写表单。

**WTForms表单**

安装Flask-WTF拓展：`pipenv install flask-wtf`

设置密钥：`app.secret_key = 'secret string'`

```py
>>> from wtforms import Form, StringField, PasswordField, BooleanField, SubmitField
>>> from wtforms.validators import DataRequired, Length
>>> class LoginForm(Form):
```

## 留言板项目

最终效果：

![image](https://user-images.githubusercontent.com/88172940/217724711-c6ce180c-e576-4603-8612-dce172edeeb5.png)

### 前置环境

```shell
git clone https://github.com/greyli/sayhello.git
cd sayhello
pipenv install # 可能因为自己已经安装过，会导致命令失败
pipenv shell # 能够启动虚拟环境就好
pip install -U bootstrap-flask
pip install -U python-dotenv
pip install -U flask_moment
pip install -U flask_sqlalchemy
pip install -U flask_wtf
pip install -U Faker
pip install -U flask-debugtoolbar

flask forge
flask run
```

### 文件结构

![image](https://user-images.githubusercontent.com/88172940/217708534-09fd51fa-3921-42c3-a1d9-590d0b306778.png)

![image](https://user-images.githubusercontent.com/88172940/217708356-454914c8-0644-449a-876a-160d11e65a0b.png)

![image](https://user-images.githubusercontent.com/88172940/217708151-dd9a58da-ae94-4729-bf7f-f6a66b4a41b6.png)



### 1. 配置文件

```py
import os
import sys

from sayhello import app

# 兼容windows系统和其他系统
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

# 数据库URL配置，app.root_path来标识数据库文件路径，数据库文件命名为data.db
dev_db = prefix + os.path.join(os.path.dirname(app.root_path), 'data.db')

SECRET_KEY = os.getenv('SECRET_KEY', 'secret string') # 密钥
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', dev_db)
```

在构造文件`__init__.py`中引入配置：`app.config.from_pyfile('settings.py')`

### 2. 创建程序实例

`__init__.py`：

```py
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

app = Flask('sayhello')
app.config.from_pyfile('settings.py') # 引入配置文件
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

db = SQLAlchemy(app) # 创建数据库对象
bootstrap = Bootstrap(app) # bootstrap对象
moment = Moment(app) # moment对象

from sayhello import views, errors, commands # 导入自定义的模块到构造文件中
# 为了让使用程序实例app注册的视图函数，错误处理函数，自定义命令函数等和程序实例关联起来，我们需要在构造文件中导入这些模块。因为这些模块也需要从构造文件中导入程序实例，所以为了避免循环依赖，这些导入语句在构造文件的末尾定义。
```

### 3. 前端建模

常用的原型设计工具有Axure RP（https://www.axure.com/ ）、Mockplus（https://www.mockplus.cn/ ）等。



### 4. 后端建模

templates/models.py:

```jinja2
from datetime import datetime
from sayhello import db

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True) {% 主键，id %}
    body = db.Column(db.String(200)) {% 消息内容 %}
    name = db.Column(db.String(20)){% 用户名 %}
    timestamp = db.Column(db.DateTime, default=datetime.now, index=True){% 时间戳 %}
```

templates/forms.py:

```py
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class HelloForm(FlaskForm): # 表单类
    name = StringField('Name', validators=[DataRequired(), Length(1, 20)])
    body = TextAreaField('Message', validators=[DataRequired(), Length(1, 200)])
    submit = SubmitField()
```

视图函数templates/views.py，主要处理GET请求和POST请求：

```py
from flask import flash, redirect, url_for, render_template

from sayhello import app, db
from sayhello.forms import HelloForm
from sayhello.models import Message


# class HelloForm(FlaskForm): # 表单类
#     name = StringField('Name', validators=[DataRequired(), Length(1, 20)])
#     body = TextAreaField('Message', validators=[DataRequired(), Length(1, 200)])
#     submit = SubmitField()
@app.route('/', methods=['GET', 'POST']) # 路由绑定修饰器
def index():
    form = HelloForm()
    if form.validate_on_submit(): # 有效则加入
        name = form.name.data
        body = form.body.data
        message = Message(body=body, name=name)
        db.session.add(message)
        db.session.commit()
        flash('Your message have been sent to the world!')
        return redirect(url_for('index'))

    messages = Message.query.order_by(Message.timestamp.desc()).all() # 排序
    return render_template('index.html', form=form, messages=messages) # 传入参数，使用index.html模板渲染
```



### 5. 编写模板

编写基模板templates/base.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>{% block title %}Say Hello!{% endblock %}</title>
    <link rel="icon" href="{{ url_for('static', filename='favicon.ico') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/bootstrap.min.css') }}" type="text/css">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}" type="text/css">
</head>
<body>

<main class="container">
    <header>
        <h1 class="text-center display-4">
            <a href="{{ url_for('index') }}" class="text-success"><strong>Say Hello</strong></a>
            <small class="text-muted sub-title">to the world</small>
        </h1>
    </header>


    {% for message in get_flashed_messages() %}
        <div class="alert alert-info">
            <button type="button" class="close" data-dismiss="alert">&times;</button>
            {{ message }}
        </div>
    {% endfor %}
    {% block content %}{% endblock %}


    <footer class="text-center">
        {% block footer %}
            <small> &copy; 2018 <a href="http://greyli.com" title="Written by Grey Li">Grey Li</a> /
                <a href="https://github.com/greyli/sayhello" title="Fork me on GitHub">GitHub</a> /
                <a href="http://helloflask.com" title="A HelloFlask project">HelloFlask</a>
            </small>
            <p><a id="bottom" href="#" title="Go Top">&uarr;</a></p>
        {% endblock %}
    </footer>
</main>


<script type="text/javascript" src="{{ url_for('static', filename='js/jquery-3.2.1.slim.min.js') }}"></script>
<script type="text/javascript" src="{{ url_for('static', filename='js/popper.min.js') }}"></script>
<script type="text/javascript" src="{{ url_for('static', filename='js/bootstrap.min.js') }}"></script>
<script type="text/javascript" src="{{ url_for('static', filename='js/script.js') }}"></script>
{{ moment.include_moment(local_js=url_for('static', filename='js/moment-with-locales.min.js')) }}
</body>
</html>
```

templates/index.html

```html
{% extends 'base.html' %}
{#从bootstrap中引入渲染表格模板类#}
{% from 'bootstrap/form.html' import render_form %}

{% block content %}
    <div class="hello-form">
        {{ render_form(form, action=request.full_path) }}
    </div>
    <h5>{{ messages|length }} messages
        <small class="float-right">
            <a href="#bottom" title="Go Bottom">&darr;</a>
        </small>
    </h5>
    <div class="list-group">
        {% for message in messages %}
            <a class="list-group-item list-group-item-action flex-column">
                <div class="d-flex w-100 justify-content-between">
                    <h5 class="mb-1 text-success">{{ message.name }}
                        <small class="text-muted"> #{{ loop.revindex }}</small>
                    </h5>
                    <small data-toggle="tooltip" data-placement="top"
                           data-timestamp="{{ message.timestamp.strftime('%Y-%m-%dT%H:%M:%SZ') }}"
                           data-delay="500">
                        {{ moment(message.timestamp).fromNow(refresh=True) }}
                    </small>
                </div>
                <p class="mb-1">{{ message.body }}</p>
            </a>
        {% endfor %}
    </div>
{% endblock %}
```

### 6. Faker生成虚拟数据

commands.py

```py
import click

from sayhello import app, db
from sayhello.models import Message


@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop): # 初始化数据库命令
    if drop:
        click.confirm('This operation will delete the database, do you want to continue?', abort=True)
        db.drop_all()
        click.echo('Drop tables.')
    db.create_all()
    click.echo('Initialized database.')


@app.cli.command()
@click.option('--count', default=20, help='Quantity of messages, default is 20.')
def forge(count): # 这个命令用来创建虚拟数据，count表示创建虚拟message的条数，flask forge --count=40
    from faker import Faker

    db.drop_all()
    db.create_all()

    fake = Faker('zh_CN')
    click.echo('Working...')

    for i in range(count):
        message = Message(
            name=fake.name(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year()
        )
        db.session.add(message)

    db.session.commit()
    click.echo('Created %d fake messages.' % count)
```

