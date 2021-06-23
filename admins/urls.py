from django.urls import path

from admins.views import index, AdminUsersListView, admin_users_update, admin_users_delete, AdminUsersCreateView, admin_users_return

app_name = 'admins'

urlpatterns = [
    path('', index, name='index'),
    path('users/', AdminUsersListView.as_view(), name='admin_users'),
    path('users/create/', AdminUsersCreateView.as_view(), name='admin_users_create'),
    path('users/update/<int:id>', admin_users_update, name='admin_users_update'),
    path('users/delete/<int:id>', admin_users_delete, name='admin_users_delete'),
    path('users/return/<int:id>', admin_users_return, name='admin_users_return'),
]
