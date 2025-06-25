from django.urls import path
from . import views

app_name = 'coreApp'

urlpatterns = [
    # Changed from 'admin/' to 'manage/'
    path('manage/chapter/add/', views.create_chapter, name='create_chapter'),
    path('manage/chapter/<int:pk>/edit/', views.edit_chapter, name='edit_chapter'),
    path('manage/topic/add/', views.create_topic, name='create_topic'),
    path('manage/topic/add/<int:chapter_pk>/', views.create_topic, name='create_topic_for_chapter'),
    path('manage/topic/<int:pk>/edit/', views.edit_topic, name='edit_topic'),
    path('manage/dashboard/', views.admin_dashboard, name='admin_dashboard'),
]