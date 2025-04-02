from django.urls import path
from . import views

urlpatterns = [
  path('', views.get_users, name="get_users"),
  path('<uuid:user_id>/', views.get_user, name="get_user"),
  path('create/', views.create_user, name="create_user"),
  path('update/<uuid:user_id>/', views.update_user, name="update_user"),
  path('delete/<uuid:user_id>/', views.delete_user, name="delete_user"),
]