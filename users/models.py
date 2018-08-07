from django.db import models
from django.contrib.auth.models import AbstractUser


# 自定义用户对象
class User(AbstractUser):
    nickname = models.CharField(max_length=50, blank=True)
    email = models.EmailField('邮箱', unique=True, error_messages={'unique': "该邮箱地址已被占用。", }, )

    class Meta(AbstractUser.Meta):
        pass
