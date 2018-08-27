from django.urls import path
from chart import views as cv
from django.conf.urls import url, include


app_name = 'chart'

urlpatterns = [
    path('', cv.index),
    url(':/', cv.rest),
]

