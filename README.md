# pac by cczzrs


#### 项目介绍
爬虫、页面列表数据、页面详情数据、增量监控、爬取规则录入、规则列表、规则管理、
    并发队列、爬取进度 chart图展示、登录注册、管理员后台等。
地址 http://0-0.cc/pac


#### 软件架构
linux docker mysql
nginx uwsgi python3 django pymysql rest selenium chrome lxml


#### 安装教程

1. 环境 python nginx uwsgi python3 django selenium chrome lxml ...
2. 运行 uwsgi --ini ./pac/my_uwsgi.ini
2. 运行 nginx -c ./pac/nginx.conf
3. 详情查看 http://0-0.cc/pac/wiki


#### 使用说明

1. 环境变量
    chrome
    chromedriver

2.数据库配置
    DATABASES_ENGINE =  'django.db.backends.mysql'  # 数据库的类型
    DATABASES_NAME =    'pactera'   if this_os else 'pac'              # 所使用的的数据库的名字
    DATABASES_USER =    'root'      if this_os else 'root'             # 数据库服务器的用户
    DATABASES_PASSWORD ='root'      if this_os else 'root'             # 密码
    DATABASES_HOST =    '0-0.cc'    if this_os else 'mysql'            # 主机
    DATABASES_PORT =    '3306'      if this_os else '3306'             # 端口

3.静态文件 static 集成路径 (nginx static file path)
    STATIC_ROOT = r'C:/Users/static_data/' if this_os else r'/home/pac/static_data/'

3. 详情查看 ./pac/settings.py


#### find me
cczzrs@aliyun.com
http://0-0.cc
