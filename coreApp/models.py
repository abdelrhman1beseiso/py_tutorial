from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.html import mark_safe
from markdown import markdown

class Chapter(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('chapter_detail', kwargs={'pk': self.pk})

class Topic(models.Model):
    EASY = 'easy'
    MEDIUM = 'medium'
    HARD = 'hard'
    
    DIFFICULTY_CHOICES = [
        (EASY, 'Beginner'),
        (MEDIUM, 'Intermediate'),
        (HARD, 'Advanced'),
    ]

    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='topics')
    title = models.CharField(max_length=100)
    content = models.TextField()
    rendered_content = models.TextField(editable=False, default='') 
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default=MEDIUM)
    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.rendered_content = markdown(self.content)
        super().save(*args, **kwargs)
    
    def save(self, *args, **kwargs):
        # Render markdown to HTML before saving
        self.rendered_content = markdown(self.content)
        super().save(*args, **kwargs)
    
    def get_rendered_content(self):
        return mark_safe(self.rendered_content)
