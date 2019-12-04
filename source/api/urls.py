from django.urls import path, include
from .views import TaskViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'tasks', TaskViewSet)

app_name = 'api'


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]