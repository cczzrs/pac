from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.conf.urls import url, include
from REST import urls as rest_urls


app_name = 'index'


def index(request):  # 登录后及进入提醒首页（网站数据增量监控提醒模块）
    return render(request, 'TXSP/index.html' if request.user.is_authenticated else 'index.html')


def msg(request):  # msg 留言
    return render(request, 'msg/index.html' if request.user.is_authenticated else 'index.html')


def wiki(request):  # wiki 文档
    return render(request, 'wiki/index.html' if request.user.is_authenticated else 'index.html')


urlpatterns = [
    path('pac/', index, name='index'),  # 默认进入首页
    path('pac/msg/', msg, name='msg'),  # msg 留言
    path('pac/wiki/', wiki, name='wiki'),  # wiki 文档

    path('pac/rest/', include(rest_urls.router.urls)),  # rest
    path('pac/rest/', include('rest_framework.urls', namespace='rest_framework')),

    path('pac/admin/', admin.site.urls),  # admin 管理员

    path('pac/users/', include('users.urls')),  # USERS 用户
    path('pac/users/', include('django.contrib.auth.urls')),  # 将 auth 应用中的 urls 模块包含进来

    path('pac/set/', include('core.urls'), name='core'),  # 爬虫数据规则检索 体系

    path('pac/txv/', include('TXSP.urls'), name='TXSP'),  # 爬虫数据检索提醒 体系

    path('pac/chart/', include('chart.urls'), name='chart'),  # 爬虫数据图形展示
]
