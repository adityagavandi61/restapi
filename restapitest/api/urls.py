from django.contrib import admin
from django.urls import path,include
from api import views


urlpatterns = [
    path("create_user/", views.create_user, name="create_user"),
    path("users/", views.read_users, name="read_users"),
    path("users/<int:user_id>/", views.read_user_by_id, name="read_user_by_id"),
    path("update_user/<int:user_id>/", views.update_user, name="update_user"),
    path("delete_user/<int:user_id>/", views.delete_user, name="delete_user"),
]