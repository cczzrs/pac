from django.urls import path
from core import views as cv
from django.conf.urls import url, include


app_name = 'core'

urlpatterns = [
    path('', cv.index),
    url('s/', cv.pathRun),
    path('test', cv.test),
    path('test2', cv.test2),
]

