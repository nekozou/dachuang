## 创建虚拟环境

虚拟环境是独立于 Python 全局环境的 Python 解释器环境，在Linux环境下激活：`. env/bin/activate`，本质上就是运行一个程序（注意需要在项目文件夹中运行该命令）。

Flask 是典型的微框架，作为 Web 框架来说，它仅保留了核心功能：**请求响应处理**和**模板渲染**。这两类功能分别由 Werkzeug（WSGI 工具库）完成和 Jinja（模板渲染库）完成。

## 第一个程序

装饰器作用：让其他函数在不需要做任何代码变动的前提下增加额外功能，装饰器的也是一个[函数对象](https://www.zhihu.com/search?q=函数对象&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"answer"%2C"sourceId"%3A99243411})。它经常用于有切面需求的场景，比如：插入日志、[性能测试](https://www.zhihu.com/search?q=性能测试&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"answer"%2C"sourceId"%3A99243411})、事务处理、缓存、权限校验等场景。装饰器是解决这类问题的绝佳设计，有了装饰器，我们就可以抽离出大量与函数功能本身无关的雷同代码并继续重用。概括的讲，装饰器的作用就是为已经存在的对象添加额外的功能。

```py
from flask import Flask # 从flask包中导入Flask类

app = Flask(__name__) # 实例化一个Flask类，__name__可以认为是普适参数

@app.route('/') # hello函数的装饰器
def hello():
    return 'Welcome to My Watchlist!'
```

注意这里隐藏了 一个**程序发现机制**，Flask 默认会假设你把程序存储在名为 app.py 或 wsgi.py 的文件中。如果你使用了其他名称，就要设置系统环境变量 `FLASK_APP` 来告诉 Flask 你要启动哪个程序：`$ export FLASK_APP=hello.py`

* `FLASK_APP`变量，存储敏感数据。

* `FLASK_ENV`变量，设置为`development`适用于调试。

用来设置程序运行的环境，默认为 `production`。调试模式可以通过将系统环境变量 `FLASK_ENV` 设为 `development` 来开启。调试模式开启后，当程序出错，浏览器页面上会显示错误信息；代码出现变动后，程序会自动重载。

`$ export FLASK_ENV=development  # 注意在 Windows 系统使用 set 或 $env: 替代 export，参考前面的示例`。

安装用来自动导入系统环境变量的 python-dotenv：

当 python-dotenv 安装后，Flask 会从项目根目录的 .flaskenv 和 .env 文件读取环境变量并设置。我们分别使用文本编辑器创建这两个文件，或是使用更方便的 `touch` 命令创建（注意不要漏掉文件名开头的点）。

## 修改视图函数名

代表某个路由的端点（endpoint），同时用来生成视图函数对应的 URL。对于程序内的 URL，为了避免手写，Flask 提供了一个 `url_for` 函数来生成 URL，它接受的第一个参数就是端点值，默认为视图函数的名称。

```py
from flask import url_for
from markupsafe import escape

# ...

@app.route('/')
def hello():
    return 'Hello'

@app.route('/user/<name>')
def user_page(name):
    return f'User: {escape(name)}'

@app.route('/test')
def test_url_for():
    # 下面是一些调用示例（请访问 http://localhost:5000/test 后在命令行窗口查看输出的 URL）：
    print(url_for('hello'))  # 生成 hello 视图函数对应的 URL，将会输出：/
    # 注意下面两个调用是如何生成包含 URL 变量的 URL 的
    print(url_for('user_page', name='greyli'))  # 输出：/user/greyli
    print(url_for('user_page', name='peter'))  # 输出：/user/peter
    print(url_for('test_url_for'))  # 输出：/test
    # 下面这个调用传入了多余的关键字参数，它们会被作为查询字符串附加到 URL 后面。
    print(url_for('test_url_for', num=2))  # 输出：/test?num=2
    return 'Test page'
```

## 模板

按照默认的设置，Flask 会从程序实例所在模块同级目录的 templates 文件夹中寻找模板，我们的程序目前存储在项目根目录的 app.py 文件里，所以我们要在项目根目录创建这个文件夹。

Jinja2 的语法和 Python 大致相同，你在后面会陆续接触到一些常见的用法。在模板里，你需要添加特定的定界符将 Jinja2 语句和变量标记出来，下面是三种常用的定界符：

- `{{ ... }}` 用来标记变量。
- `{% ... %}` 用来标记语句，比如 if 语句，for 语句等。
- `{# ... #}` 用来写注释。

app.py代码：

```py
name = 'Grey Li'
movies = [
    {'title': 'My Neighbor Totoro', 'year': '1988'},
    {'title': 'Dead Poets Society', 'year': '1989'},
    {'title': 'A Perfect World', 'year': '1993'},
    {'title': 'Leon', 'year': '1994'},
    {'title': 'Mahjong', 'year': '1996'},
    {'title': 'Swallowtail Butterfly', 'year': '1996'},
    {'title': 'King of Comedy', 'year': '1999'},
    {'title': 'Devils on the Doorstep', 'year': '1999'},
    {'title': 'WALL-E', 'year': '2008'},
    {'title': 'The Pork of Music', 'year': '2012'},
] # 定义数据

from flask import Flask, render_template

app = Flask(__name__) # 实例化
# ...

@app.route('/')
def index():
    return render_template('index.html', name=name, movies=movies) # 使用render_template函数渲染，传入参数
```

template/index.html代码：

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>{{ name }}'s Watchlist</title>
</head>
<body>
    <h2>{{ name }}'s Watchlist</h2>
    {# 使用 length 过滤器获取 movies 变量的长度 #}
    <p>{{ movies|length }} Titles</p> 
    <!--这里调用了movies的某个过滤器，获取某个值-->
    <ul>
        {% for movie in movies %}  {# 迭代 movies 变量 #}
        <li>{{ movie.title }} - {{ movie.year }}</li>  {# 等同于 movie['title'] #}
        {% endfor %}  {# 使用 endfor 标签结束 for 语句 #}
    </ul>
    <footer>
        <small>&copy; 2018 <a href="http://helloflask.com/book/3">HelloFlask</a></small>
    </footer>
</body>
</html>
```

效果如图：

![image](https://user-images.githubusercontent.com/88172940/215946359-f02d3c8b-eaf4-4768-b370-c8b92154dcd6.png)

## 静态文件

静态文件（static files）和我们的模板概念相反，指的是内容不需要动态生成的文件。比如图片、CSS 文件和 JavaScript 脚本等。

可以使用url_for()函数生成路由。

## 数据库

借助 SQLAlchemy，你可以通过定义 Python 类来表示数据库里的一张表（类属性表示表中的字段 / 列），通过对这个类进行各种操作来代替写 SQL 语句。这个类我们称之为**模型类**，类中的属性我们将称之为**字段**。

为了设置 Flask、扩展或是我们程序本身的一些行为，我们需要设置和定义一些配置变量。Flask 提供了一个统一的接口来写入和获取这些配置变量：`Flask.config` 字典。配置变量的名称必须使用大写，写入配置的语句一般会放到扩展类实例化语句之前。下面写入了一个 `SQLALCHEMY_DATABASE_URI` 变量来告诉 SQLAlchemy 数据库连接地址：

```sql
import os

# ...

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.path.join(app.root_path, 'data.db')
# salite://// + 数据库的绝对地址，app.root_paht返回程序实例所在模块的路径，目前使用app，即根目录
```

在代码中创建了模型类：

```py
class User(db.Model):  # 表名将会是 user（自动生成，小写处理）
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(20))  # 名字


class Movie(db.Model):  # 表名将会是 movie
    id = db.Column(db.Integer, primary_key=True)  # 主键
    title = db.Column(db.String(60))  # 电影标题
    year = db.Column(db.String(4))  # 电影年份
```

还需要创建表和数据库文件

```shell
(env) $ flask shell
>>> from app import db
>>> db.create_all()
```

**自定义命令来自动执行创建数据库表操作**

app.py

```py
import click


@app.cli.command()  # 注册为命令，可以传入 name 参数来自定义命令
@click.option('--drop', is_flag=True, help='Create after drop.')  # 设置选项
def initdb(drop):
    """Initialize the database."""
    if drop:  # 判断是否输入了选项
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')  # 输出提示信息
```

## 404页面

templates/404.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>{{ user.name }}'s Watchlist</title>
    <link rel="icon" href="{{ url_for('static', filename='favicon.ico') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}" type="text/css">
</head>
<body>
    <h2>
        <img alt="Avatar" class="avatar" src="{{ url_for('static', filename='images/avatar.png') }}">
        {{ user.name }}'s Watchlist
    </h2>
    <ul class="movie-list">
        <li>
            Page Not Found - 404
            <span class="float-right">
                <a href="{{ url_for('index') }}">Go Back</a>
            </span>
        </li>
    </ul>
    <footer>
        <small>&copy; 2018 <a href="http://helloflask.com/book/3">HelloFlask</a></small>
    </footer>
</body>
</html>
```



## 表单

默认情况下，当表单中的提交按钮被按下，浏览器会创建一个新的请求，默认发往当前 URL（在 `<form>` 元素使用 `action` 属性可以自定义目标 URL）。

因为我们在模板里为表单定义了 POST 方法，当你输入数据，按下提交按钮，一个携带输入信息的 POST 请求会发往根地址。接着，你会看到一个 405 Method Not Allowed 错误提示。这是因为处理根地址请求的 `index` 视图默认只接受 GET 请求。

> **提示** 在 HTTP 中，GET 和 POST 是两种最常见的请求方法，其中 GET 请求用来获取资源，而 POST 则用来创建 / 更新资源。我们访问一个链接时会发送 GET 请求，而提交表单通常会发送 POST 请求。





后期数据库部分重构出现问题，导致删去了原有`data.db`文件，无法重构。

## 最终成果

![image](https://user-images.githubusercontent.com/88172940/216047637-e7db8f22-fd76-4e82-a4ab-740f2b1d026c.png)
