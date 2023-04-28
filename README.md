### 项目运行

1、保证`Python`环境在3.6以上或更高版本（3.6之前可能不支持`pipenv`）。

2、（Windows）`PATH`环境变量包含`Python`可执行文件目录。

3、`pip install pipenv`：安装`pipenv`，后续通过`pipenv`工具来进行依赖管理（也可以使用`pip + virtualenv`）；其中Linux或者macOS系统最好使用`sudo pip install pipenv`命令进行全局安装。

4、`pipenv install`：通过pipenv工具安装`requirements.txt`文件中的依赖。如果之前已经运行过该命令，可以使用`pipenv install --dev`命令只安装开发相关依赖。

5、`pipenv shell`：显式激活虚拟环境。

6、在激活的虚拟环境中，使用`pipenv install flask`命令安装`Flask`框架。

**注：**在Pycharm等IDE中，需要将解释器路径设置为对应的虚拟环境路径，通常macOS中路径类似：`~/.local/share/virtualenvs/helloflaskkSN7ec1K/bin/python`；Windows中路径类似：`C：\Users\Administrator\.virtualenvs\helloflask-5Pa0ZfZw\Scripts\python.exe`。

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

### 登录

可以在后台`view.py`文件中修改账号密码。

* 账号：`zyg`
* 密码：`123`
