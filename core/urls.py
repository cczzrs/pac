from django.urls import path
from core import views as cv
from django.conf.urls import url, include


app_name = 'core'

urlpatterns = [
    path('', cv.index_db),
    path('look/', cv.index_look),
    path('edit/', cv.index_edit),
    path('c/', cv.index_cl),
    path('i/', cv.index_mg),
    path('i/del/', cv.index_del),
    path('i/qiy/', cv.index_qiy),
    url('s/', cv.pathRun),
    path('test1', cv.test1),
    path('test2', cv.test2),
]

