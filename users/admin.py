from django.contrib import admin
from .models import User
from core.models import SpidersBaseSource


admin.site.register(User)  # 注册用户

admin.site.register(SpidersBaseSource)  # 爬虫主数据


