## 构建项目并运行 pac ( build and run pac )（该操作是构建 Dockerfile 后的容器实例中操作）

# 进入 home 目录
cd /home/

# 克隆下载代码到当前目录
git clone https://github.com/cczzrs/pac.git

# 检查需要更新的表
python /home/pac/manage.py makemigrations

# 更新表到数据库，如果数据库已存在某个表则会报错，删除（删除需谨慎！[数据]）该表，再执行即可
python /home/pac/manage.py migrate

# 创建管理员账号（根据提示操作即可）
python manage.py createsuperuser

# 生成静态文件，做 nginx 指向用，路径默认为 '/home/pac/static_data/static'，修改在：./pac/settings.py:STATIC_ROOT
python3 /home/pac/manage.py collectstatic

# 运行 uwsgi 启动 pac 项目
uwsgi --ini /home/pac/my_uwsgi.ini

# 运行 nginx 监控 http 请求 80 端口，（这里需要修改监控 IP 地址（你机器的外网地址）在：./pac/nginx.conf:server_name）
nginx -c /home/pac/nginx.conf

# 查看进程，监控 uwsgi 日志
ps && tail -fn 30 /home/uwsgi/wsgi_mysite.log