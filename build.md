### pac 爬虫系统部署，（两个 docker 镜像 [cczzrs/pac:latest][cczzrs/pac:mysql]）

# 创建与容器的共享目录
mkdir /home/docker/

# 进入到该目录下
cd /home/docker/

# 下载 pac 项目源码到该目录下（没有 git 命令，需自行安装一下）
git clone https://github.com/cczzrs/pac.git

# 进入到项目目录下
cd ./pac/


# 构建 docker pac 环境镜像 cczzrs/pac:latest ，监控 80 端口，共享文件目录 /home/docker/ ， 关联 MYSQL 容器
docker build -t cczzrs/pac:latest .
# 或者 or
# 下载 pac 运行需要的镜像环境 cczzrs/pac:latest
# docker pull cczzrs/pac:latest

# 构建 docker mysql 环境镜像 cczzrs/pac:mysql
docker build -t cczzrs/pac:mysql -f ./Dockerfile_mysql .
# 或者 or
# 下载 pac 数据存储 mysql 的镜像环境 cczzrs/pac:mysql
# docker pull cczzrs/pac:mysql


# 运行 cczzrs/pac:mysql 容器 MYSQL ，监控 3306 端口，共享文件目录 /home/docker/
docker run -p 3306:3306 -v /home/docker/:/home/docker/ -e MYSQL_DATABASE=admin -e MYSQL_ROOT_PASSWORD=admin -e MYSQL_USER=root -e MYSQL_PASSWORD=root --name MYSQL -itd cczzrs/pac:mysql sh /build_mysql.sh

# 进入容器 MYSQL
docker exec -it MYSQL sh

# 进入 mysql 数据库
mysql -u root

# 初始化表和数据，[表(init_db.sql) 或者 表和数据(init_main_db.sql)]
# source /home/docker/pac/init_db.sql;
source /home/docker/pac/init_main_db.sql;

# 退出数据库
exit

# 退出容器 MYSQL
exit


# 运行 cczzrs/pac:latest 容器 pac
docker run -p 80:80 --link MYSQL:mysql  -v /home/docker/:/home/docker/ --name pac -it cczzrs/pac:latest sh

# 此时已进入容器 pac 中，进入到 /home目录下
cd /home/

# 再次下载 pac 项目源码到该目录下
git clone https://github.com/cczzrs/pac.git

# 进入到 ./pac/目录下
cd ./pac/

# 检查需要更新的表
python3 /home/pac/manage.py makemigrations

# 更新表到数据库，如果数据库已存在某个表则会报错，删除（删除需谨慎！[数据]）该表，再执行即可
python3 /home/pac/manage.py migrate

# 创建管理员账号（根据提示操作即可）
python3 manage.py createsuperuser

# 生成静态文件，做 nginx 指向用，路径默认为 '/home/pac/static_data/static'，修改在：./pac/settings.py:STATIC_ROOT
python3 /home/pac/manage.py collectstatic

# 修改外网 ip ，vim 进入 nginx.conf 第 104 行
vim +104 nginx.conf
# 按 i 开启编辑状态，把 127.0.0.1 修改为你的外网 IP
# 按 Esc 退出编辑状态，再按 Shift + ZZ 组合键保存并退出

# 运行 uwsgi 启动 pac 项目
uwsgi --ini /home/pac/my_uwsgi.ini

# 运行 nginx 监控 http 请求 80 端口，（这里需要修改监控 IP 地址（你机器的外网地址）在：./pac/nginx.conf:server_name）
nginx -c /home/pac/nginx.conf

# 查看进程，监控 uwsgi 日志
ps && tail -fn 30 /home/uwsgi/wsgi_mysite.log

# 无错误即可通过浏览器访问 http://IP/pac

# 注意退出时需要后台改容器，按 Ctrl + p + q 组合键即可退出并后台容器