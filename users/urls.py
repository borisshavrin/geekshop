from django.urls import path

from users.views import UsersLoginView, UsersRegisterViews, logout, UsersProfileView, verify

app_name = 'users'

urlpatterns = [
    path('login/', UsersLoginView.as_view(), name='login'),
    path('register/', UsersRegisterViews.as_view(), name='register'),
    # path('register/', register, name='register'),
    path('profile/<int:pk>', UsersProfileView.as_view(), name='profile'),
    path('logout/', logout, name='logout'),
    path('verify/<str:email>/<str:activation_key>/', verify, name='verify'),
]
