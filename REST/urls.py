from django.conf.urls import include, url
from django.urls import path
from rest_framework import routers
from REST import views


app_name = 'REST'

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'BaseSource', views.BaseSourceViewSet)

urlpatterns = [
    # path('rest/', include(rest_urls.router.urls)),  # rest
    # path('rest/', include('rest_framework.urls', namespace='rest_framework')),
]
