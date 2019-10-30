from django.urls import path
from accounts.views import login_view, logout_view, register_view, user_activate, UserDetailView,\
    UserInfoChangeView

app_name = 'accounts'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('register/activate/', user_activate, name='user_activate'),
    path('<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('<int:pk>/update', UserInfoChangeView.as_view(), name='user_update')
]