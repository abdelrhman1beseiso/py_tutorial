from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name='UserApp'
urlpatterns = [
    path('', views.home, name='home'),  
    path('course/', views.enter_course, name='enter_course'),
    path('chapter/<int:pk>/', views.chapter_detail, name='chapter_detail'),
    path('topic/<int:pk>/', views.topic_detail, name='topic_detail'),
    path('progress/', views.user_progress, name='user_progress'),
    path('complete/<int:topic_id>/', views.mark_complete, name='mark_complete'),
]