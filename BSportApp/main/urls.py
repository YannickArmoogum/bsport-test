from django.urls import path, include
from rest_framework import routers
from .views import *
from django.conf.urls import url
from . import views 

router = routers.DefaultRouter()
router.register(r'user', views.UserProfileView, basename='user')
router.register(r'appointment', views.AppointmentView, basename='appointment')
#router.register(r'api/DynamoDB',views.DynamoDB.as_view(), basename='DynamoDB')


urlpatterns = [
    url(r'^api/', include((router.urls,'main'),namespace='main')),
    path(r'DynamoDB',views.DynamoDB.as_view(), name='Get all dynamoDB appointment data')
]