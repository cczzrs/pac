from django.urls import path
from TXSP import views as txv


app_name = 'TXSP'

urlpatterns = [
    path('', txv.index),
    path('run', txv.test_list_page),
    path('run/dbo', txv.get_test_list_dbo),
    path('run/isdbo', txv.get_test_is_runing),
    path('run/stop', txv.stop_test_list_page),
    path('run/clear', txv.clear_test),
]

