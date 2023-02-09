Flask学习笔记
基础篇
开发环境
出现bug：pip无法使用；查阅资料发现需要升级到最新版本。
创建虚拟环境并激活
content_copy
pip install pipenv
pipenv shell
3.安装flask

content_copy
pipenv intall flask
4.配置pycharm环境

创建程序实例
flask路由：
参数：method、endpoint
动态路由
蓝图：构建目录结构
路由加载的源码流程
将url和函数打包成为rule对象
将rule对象添加到map对象中
app.url_map =map对象
过滤器
控制语句
特殊装饰器（也叫钩子）：
@app.before_request
@app.after_request
在蓝图中定义作用域是本蓝图
flask内部原理
flask框架是基于werkzeug的wsgi实现，flask自己没有wsgi
用户请求一旦到来，就会调用app.__call__方法
flask与http
GET、POST
URL处理
请求钩子
响应请求
获取数据
request.arg.get()
request.form
返回数据：
render_template()
jsonify()
redirect
cookie
content_copy
from flask import Flask, make_response @app. route (' /set/<name>' ) 
def set_cookie(name): 
    response=make_response(redirect(url_for( ' hello ' ))) 
    response . set_ cookie ( ' name ' , name) 
    return response
session：对话
视图：FBV(function)、CBV（class）
content_copy
#登录认证
def login():    
    if request.method =='GET':       
        returnrender_template('login.html')    
        user=request.form.get('user')    
        pwd=request.form.get('password')    
    if user=='zyg':        
        return redirect(url_for('index'))    
    else:        
        return('用户名错误')
flask上下文：
9f835fbf944b096196bcabc1e8e6a060.png
因为 存储在程序上下文中，而程序上下文会随着每一个请求的进入而激活，随着每一个请求的处理完毕而销毁，所以每次请求都会重设这个值 我们通常会使用它结合请求钩子来保存每个请求处理前所需要的全局变量，比如当前登入的用户对象，数据库连接等

content_copy
from flask import g
@app.before_request 
def get_name() : 
    g.name = request. args.get ('name') 
需要在没有激活上下文的情况下使用这些变量，可手动激活上下文,使用with语句或者push（）方法

模板
jinja2
渲染模板：render_template()//传值
content_copy
return render_template("xx.html",xx=xx,f=func)#可以传入函数
全局对象:为模板提供公共的方法
2a8c3a795601f2ae314b218ea70b2fc7.png
自定义：
content_copy
@app.template_global()
def func():
    pass
过滤器：过滤器和变量用一个竖线（管道符号）隔开，需要参数的过滤器可以像函数一样使用括号传递。下面是一个对 name 变量使用 title 滤器的例子 ：{{ nameltitle }}
98759cbfb76e6cafb97905e902242fee.png
//这里只列出了一部分常用的过滤器

自定义过滤器
content_copy
from flask import Markup 
@app.template_filter() 
def musical(s) : 
    return s + Markup ( ' &#9835 ; ' )
测试器：测试器 (Test) 是一些用来测试变量或表达式，返回布尔值 Tru Fa se) 特殊函数
content_copy
{% if age is number %) 
{{age* 365 ) ) 
{% else %) 
无效的数字 
{% endif %)
局部模板：插入到其他普通模板中 include
宏 macro:它类似 Python 中的函数 使用宏可以把 部分模板代码封装到宏里，使用传递的参数来构建内容，最后返回构建后的内容 在功能上， 它和局部模板类似，都是为了方便代码块的重用
content_copy
#创建
{% macro qux(amount=1)%}
    {% if amount ==1%}
        i am qux
    {% elif amount>1%}
        we are quxs
{% endmacro%}

#使用
{% from 'macros.html' import qux %}
    {{ qux(amount=5)}}
模板继承 extend
加载静态文件：url_for
自定义错误页面
表单
form
使用Flask-WTF
验证表单数据
content_copy
from flask import Flask, render_template , redirect , url_for, flash 
@app.route('/basic',methods=['GET','POST') 
def basic(): 
    form = LoginForm() 
    if form.validate on submit(): 
        username = form.username.data 
        flash( ' Welcome home, %s!'% username) 
        return redirect (url_for ('index')) 
        return render_template ('basic.html', form=form)
使用Flask-CKEditor集成富文本编辑器
数据库
sql和nosql
nosql:
文档存储（json）
键值对存储（redis）
ORM：相比与原生的sql语句，更简单更安全
表——>Python类
字段（列）——》类属性
记录（行）——》类实例
Flask-SQLAlchemy扩展
数据库模型（model）
content_copy
class Note(db .Model) : 
id = db.Column(db.Integer, primary_ke y=True) 
body= db Column(db.Text)
3f9331c444e3d1c112013482d624c61d.png

创建数据库和表
db.create_all()
增删改查（CRUD）
content_copy
#增 db.Model就是数据库模型的名字
note1=db.Model(body='xxx')
db.session.add(note1)
db.session.commit
#查询
note1=db.Model.query.all()
note2=Note.query.get(2)//返回主键值（id）的记录
note3=db.Model.query.filter(db.Model..body='XXX').first()
note4=db.query.filter_by(body='xxx').first()
#更改
直接赋值，然后commit
#删除
db.session.delete(xxx)
commit
建立关系
一对多
建立外键：db.ForeignKey('xx.id')
定义关系属性：db.relationship('xxx')
给外键字段赋值或者调用append()
多对多
多对一
一对一
更新数据库
删除表后重建
content_copy
#删除表后重建
@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    """Initialize the database."""
    if drop:
        click.confirm('This operation will delete the database, do you want to continue?', abort=True)
        db.drop_all()
        click.echo('Drop tables.')
    db.create_all()
    click.echo('Initialized database.')
使用flask-Migrate 迁移数据库
