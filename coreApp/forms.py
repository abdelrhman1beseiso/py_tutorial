from django import forms
from .models import Chapter, Topic

class ChapterForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = ['title', 'description', 'order']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['title','content', 'difficulty', 'is_published','order']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 20}),
        }