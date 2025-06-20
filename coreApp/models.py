from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Chapters(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title
    
class Topics(models.Model):
    chapter = models.ForeignKey(Chapters, on_delete=models.CASCADE, related_name='topics')
    title = models.CharField(max_length=100)
    content = models.TextField()
    example_code_image = models.ImageField(upload_to='example_code_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title    
    
class userProfile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    track_progress = models.ManyToManyField(Chapters, related_name='tracked_users', blank=True)
    current_chapter = models.ForeignKey(Chapters, on_delete=models.SET_NULL, null=True, blank=True, related_name='current_users')
    current_topic = models.ForeignKey(Topics, on_delete=models.SET_NULL, null=True, blank=True, related_name='current_users')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username    