# pac by cczzrs


#### 项目介绍
爬虫、页面列表数据、页面详情数据、增量监控、爬取规则录入、规则列表、规则管理、
    并发队列、爬取进度 chart图展示、登录注册、管理员后台等。
地址 http://0-0.cc/pac
文档 http://0-0.cc/pac/wiki
留言 http://0-0.cc/pac/msg


#### 项目架构
linux docker mysql
nginx uwsgi python3 django pymysql rest selenium chrome lxml


#### 项目结构
pac
 |
  -ALLSP----------空模块，
 |
  -chart----------chart图（统计图）展示模块，
 |
  -core-----------项目核心，基本数据操作模块，
 |
  -pac------------项目入口，拦截器总入口，项目本身文件，
 |
  -REST-----------rest http请求模式，配置模块，
 |
  -spiders--------封装spiders处理工具集，
 |
  -static---------项目静态资源(js/css/img)，
 |
  -templates------项目页面模板资源(html)，
 |
  -TXSP-----------项目提醒（网站数据增量监控提醒）模块，
 |
  -users----------项目用户管理模块，
 |
  -manage.py------django项目操作入口，
 |
  -my_uwsgi.ini---uwsgi 启动配置文件 my_uwsgi.ini，
 |
  -nginx.conf-----nginx 启动配置文件 nginx.conf，
 |
  -README.md------项目说明，
 |
  -settings.py----项目全局配置文件 settings.py ，

注意：各个模块也有 settings.py 文件，按就近原则
简写说明：
    pac: 爬虫
    SP: spider
    TXSP: (TX)提醒 模块
    LP: list spider 与爬取网站的列表数据有关
    IP: item spider 与爬取网站的列表数据的每个详情数据有关

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

3. 配置详情查看 ./pac/settings.py


#### find me
cczzrs@aliyun.com
http://0-0.cc
