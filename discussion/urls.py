from django.urls import path
from . import views

urlpatterns = [
    path('', views.sujet_list, name='sujet_list'),
    path('sujet/<int:pk>/', views.sujet_detail, name='sujet_detail'),
    path('sujet/new/', views.sujet_create, name='sujet_create'),
    path('toggle-dark-mode/', views.toggle_dark_mode, name='toggle_dark_mode'),
    path('message/<int:message_id>/like/', views.like_message, name='like_message'),
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/delete/<int:notification_id>/', views.delete_notification, name='delete_notification'),
    path('tag/<str:tag_name>/', views.sujet_by_tag, name='sujet_by_tag'),
]