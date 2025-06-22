from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Chapter, Topic, UserProgress
from .forms import ChapterForm, TopicForm
from django.db.models import Prefetch

# Simplified views without auth for testing
def admin_dashboard(request):
    chapters = Chapter.objects.all().prefetch_related('topics')
    return render(request, 'admin/dashboard.html', {
        'chapters': chapters,
        'title': 'Dashboard'
    })

def create_chapter(request):
    if request.method == 'POST':
        form = ChapterForm(request.POST)
        if form.is_valid():
            chapter = form.save()
            messages.success(request, 'Chapter created successfully!')
            return redirect('coreApp:admin_dashboard')
    else:
        form = ChapterForm()
    
    return render(request, 'admin/chapter_form.html', {
        'form': form,
        'title': 'Create Chapter'
    })

def edit_chapter(request, pk):
    chapter = get_object_or_404(Chapter, pk=pk)
    if request.method == 'POST':
        form = ChapterForm(request.POST, instance=chapter)
        if form.is_valid():
            form.save()
            messages.success(request, 'Chapter updated successfully!')
            return redirect('coreApp:admin_dashboard')
    else:
        form = ChapterForm(instance=chapter)
    
    return render(request, 'admin/chapter_form.html', {
        'form': form,
        'chapter': chapter,
        'title': 'Edit Chapter'
    })

def create_topic(request, chapter_pk=None):
    chapters = Chapter.objects.all().order_by('order')
    chapter = None
    
    if chapter_pk:
        chapter = get_object_or_404(Chapter, pk=chapter_pk)
    
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            if chapter:
                topic.chapter = chapter
            # Set order to be last in the chapter
            last_topic = Topic.objects.filter(chapter=topic.chapter).order_by('-order').first()
            topic.order = last_topic.order + 1 if last_topic else 0
            topic.save()
            messages.success(request, 'Topic created successfully!')
            return redirect('coreApp:admin_dashboard')
    else:
        initial = {'chapter': chapter.id} if chapter else {}
        form = TopicForm(initial=initial)
    
    return render(request, 'admin/topic_form.html', {
        'form': form,
        'chapters': chapters,
        'selected_chapter': chapter,
        'title': 'Create Topic'
    })
def edit_topic(request, pk):
    topic = get_object_or_404(Topic, pk=pk)
    
    # Get all chapters for the dropdown
    chapters = Chapter.objects.all()
    
    if request.method == 'POST':
        form = TopicForm(request.POST, instance=topic)
        if form.is_valid():
            form.save()
            messages.success(request, 'Topic updated successfully!')
            return redirect('coreApp:admin_dashboard')
    else:
        # Pre-select the chapter if it exists
        initial = {'chapter': topic.chapter_id} if topic.chapter else {}
        form = TopicForm(instance=topic, initial=initial)
    
    return render(request, 'admin/topic_form.html', {
        'form': form,
        'chapters': chapters,
        'selected_chapter': topic.chapter,
        'title': 'Edit Topic'
    })

def user_profile(request):
    chapters = Chapter.objects.filter(topics__is_published=True).distinct().prefetch_related(
        Prefetch('topics', queryset=Topic.objects.filter(is_published=True))
    )
    
    # Simulate progress for testing
    progress = set()
    if Topic.objects.exists():
        progress.add(Topic.objects.first().id)
    
    return render(request, 'user_profile.html', {
        'chapters': chapters,
        'completed_topics': progress,
        'title': 'My Profile'
    })