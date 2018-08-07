from users import views
from django.conf.urls import url, include
from django.urls import path


app_name = 'users'

urlpatterns = [
    url('register/', views.register, name='register'),
    # url('', include('django.contrib.auth.urls')),  # 将 auth 应用中的 urls 模块包含进来  # 移到根 url.py 下无需空间名 (app_name = 'users')
]
