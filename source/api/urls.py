from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

from .views import TaskViewSet, ProjectViewSet, LogoutView, UserCreateView
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'tasks', TaskViewSet)
router.register(r'projects', ProjectViewSet)

app_name = 'api'


urlpatterns = [
    path('', include(router.urls)),
    path('login/', obtain_auth_token, name='obtain_auth_token'),
    path('register/', UserCreateView.as_view(), name='user_register'),
    path('logout/', LogoutView.as_view(), name='delete_auth_token')
]