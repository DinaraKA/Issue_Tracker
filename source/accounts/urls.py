from django.urls import path
from accounts.views import login_view, logout_view, register_view, user_activate, UserDetailView, \
    UserInfoChangeView, UserPasswordChangeView, UserIndexView

app_name = 'accounts'

urlpatterns = [
    path('/', UserIndexView.as_view(), name='user_index'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('register/activate/', user_activate, name='user_activate'),
    path('<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('<int:pk>/update', UserInfoChangeView.as_view(), name='user_update'),
    path('<int:pk>/password_change', UserPasswordChangeView.as_view(), name='user_password_change')
]