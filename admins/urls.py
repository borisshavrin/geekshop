from django.urls import path

from admins.views import index, AdminUsersListView, AdminUsersUpdateView, AdminUsersDeleteView, AdminUsersCreateView, AdminUsersReturnView

app_name = 'admins'

urlpatterns = [
    path('', index, name='index'),
    path('users/', AdminUsersListView.as_view(), name='admin_users'),
    path('users/create/', AdminUsersCreateView.as_view(), name='admin_users_create'),
    path('users/update/<int:pk>', AdminUsersUpdateView.as_view(), name='admin_users_update'),
    path('users/delete/<int:pk>', AdminUsersDeleteView.as_view(), name='admin_users_delete'),
    path('users/return/<int:pk>', AdminUsersReturnView.as_view(), name='admin_users_return'),
]
