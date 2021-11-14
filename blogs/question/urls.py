from django.conf.urls import url
from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'query', QueryViewSet)
urlpatterns = [
      path('api/register', RegisterApi.as_view()),
      path('', include(router.urls)),
]