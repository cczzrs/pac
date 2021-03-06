
<p align="center">
    <img alt="@cczzrs" class="avatar float-left mr-1" src="https://avatars1.githubusercontent.com/u/39689748?s=460&v=4" height="158" width="158">
</p>

# pac #

[![version](https://img.shields.io/badge/release-0.1.2-lightgrey.svg)](https://github.com/cczzrs/pac)

![有图](https://github.com/cczzrs/pac/blob/master/PAC_chart.png?raw=true)

### docker ###
    * docker pull cczzrs/pac:mysql
    * docker pull cczzrs/pac:latest
 * https://hub.docker.com/r/cczzrs/pac

### 项目介绍 ###
 * 爬虫、页面列表数据、页面详情数据、增量监控、爬取规则录入、规则列表、规则管理、并发队列、爬取进度 chart图展示、登录注册、管理员后台等。
 * 在线地址 http://cczzrs.com/pac/chart/


### 项目架构 ###
 * `linux` `docker` `mysql`
 * `nginx` `uwsgi` `python3` `django` `rest` `pymysql` `lxml` `selenium` `chrome`

### 项目结构 ###
 * pac
     * ALLSP----------空模块，
     * chart----------chart图（统计图）展示模块，
     * core-----------项目核心，基本数据操作模块，
     * pac------------项目入口，拦截器总入口，项目本身文件，
     * REST-----------rest http请求模式，配置模块，
     * spiders--------封装spiders处理工具集，
     * static---------项目静态资源(js/css/img)，
     * templates------项目页面模板资源(html)，
     * TXSP-----------项目提醒（网站数据增量监控提醒）模块，
     * users----------项目用户管理模块，
     * build.md-----------在 pac 运行环境系统中构建项目并运行 pac ( build and run pac )，
     * build_mysql.sh-----在 mysql 系统中安装 mysql 数据库并运行，
     * Dockerfile---------构建 docker 镜像（image）（pac 运行环境系统），
     * Dockerfile_mysql---构建 docker 镜像（image）（mysql 系统），
     * init_db.sql--------在 mysql 系统中初始化 mysql 表结构，
     * init_main_db.sql---在 mysql 系统中初始化 mysql 表结构和数据，
     * manage.py----------django项目操作入口，
     * my_uwsgi.ini-------uwsgi 启动配置文件 my_uwsgi.ini，
     * nginx.conf---------nginx 启动配置文件 nginx.conf，
     * README.md----------项目说明，
     * settings.py--------项目全局配置文件 settings.py ，

 * 注意：各个模块也有 settings.py 文件，按就近原则
 
 * 简写说明：
     * pac: 爬虫
     * SP: spider
     * TXSP: (TX)提醒 模块
     * LP: list spider 与爬取网站的列表数据有关
     * IP: item spider 与爬取网站的列表数据的每个详情数据有关

### 安装教程 ###

 * 环境 python nginx uwsgi python3 django selenium chrome lxml ...
 * 运行 uwsgi --ini ./pac/my_uwsgi.ini
 * 运行 nginx -c ./pac/nginx.conf
 * 安装详情查看 https://github.com/cczzrs/pac/blob/master/build.md


### 使用说明 ###

 * 环境变量
    * chrome
    * chromedriver

 * 数据库配置
    * [./pac/.settings.py]
    * DATABASES_ENGINE =  'django.db.backends.mysql'  # 数据库的类型
    * DATABASES_NAME =    'pac'       if this_os else 'pac'              # 所使用的的数据库的名字
    * DATABASES_USER =    'root'      if this_os else 'root'             # 数据库服务器的用户
    * DATABASES_PASSWORD ='root'      if this_os else 'root'             # 密码
    * DATABASES_HOST =    '0-0.cc'    if this_os else 'mysql'            # 主机 mysql 为 docker link 名称
    * DATABASES_PORT =    '3306'      if this_os else '3306'             # 端口

 * 静态文件 static 集成路径 (nginx static file path)
    * [./pac/.settings.py]
    * STATIC_ROOT = r'C:/Users/static_data/' if this_os else r'/home/pac/static_data/'

 * 详情查看 https://github.com/cczzrs/pac/blob/master/build.md


### find me ###
 * cwt@cczzrs.com
 * https://cczzrs.me
