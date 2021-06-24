from django.urls import path

from users.views import UsersLoginView, UsersRegisterViews, logout, profile

app_name = 'users'

urlpatterns = [
    path('login/', UsersLoginView.as_view(), name='login'),
    path('register/', UsersRegisterViews.as_view(), name='register'),
    path('profile/', profile, name='profile'),
    path('logout/', logout, name='logout'),
]
