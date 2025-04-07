from django.urls import path
from . import views

urlpatterns = [
  path('user_types/', views.get_user_types, name='get_user_types'),
  path('', views.get_users, name="get_users"),
  path('<uuid:user_id>/', views.get_user, name="get_user"),
  path('create/', views.create_user, name="create_user"),
  path('<uuid:user_id>/update/', views.update_user, name="update_user"),
  path('<uuid:user_id>/delete/', views.delete_user, name="delete_user"),
  path('sign_in/', views.sign_in, name='sign_in'),
  path('sign_out/', views.sign_out, name='sign_out'),
  path('change_password/', views.change_password, name='change_password'),
]