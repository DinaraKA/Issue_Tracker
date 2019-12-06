from django.urls import path, include
from .views import TaskViewSet, ProjectViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'tasks', TaskViewSet)
router.register(r'projects', ProjectViewSet)

app_name = 'api'


urlpatterns = [
    path('', include(router.urls))
]