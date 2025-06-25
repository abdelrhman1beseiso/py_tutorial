from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from coreApp.models import Chapter, Topic  # Import from coreApp
from .models import UserProgress
from django.db.models import Count, Q

@login_required
def enter_course(request):
    chapters = Chapter.objects.all().prefetch_related('topics').annotate(
        total_topics=Count('topics'),
        completed_topics=Count('topics', filter=Q(topics__userprogress__user=request.user, topics__userprogress__completed=True))
    )

    total_topics = Topic.objects.count()
    completed_topics = UserProgress.objects.filter(user=request.user, completed=True).count()
    progress_percentage = (completed_topics / total_topics * 100) if total_topics > 0 else 0
    
    return render(request, 'chapter_list.html', {
        'chapters': chapters,
        'progress_percentage': round(progress_percentage),
        'total_topics': total_topics,
        'completed_topics': completed_topics,
    })

def chapter_detail(request, pk):
    chapter = get_object_or_404(Chapter, pk=pk)
    topics = chapter.topics.all().annotate(
        is_completed=Count('userprogress', filter=Q(userprogress__user=request.user, userprogress__completed=True)))
    
    return render(request, 'chapter_detail.html', {
        'chapter': chapter,
        'topics': topics,
    })

def topic_detail(request, pk):
    topic = get_object_or_404(Topic, pk=pk)
    is_completed = UserProgress.objects.filter(
        user=request.user, topic=topic, completed=True).exists()
    
    return render(request, 'topic_detail.html', {
        'topic': topic,
        'is_completed': is_completed,
    })

@login_required
def mark_complete(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    progress, created = UserProgress.objects.get_or_create(
        user=request.user, topic=topic)
    
    if not progress.completed:
        progress.completed = True
        progress.completed_at = timezone.now()
        progress.save()
        messages.success(request, f'Topic marked as completed!')
    return redirect('UserApp:topic_detail', pk=topic_id)

@login_required
def user_progress(request):
    progress = UserProgress.objects.filter(
        user=request.user, completed=True).select_related('topic', 'topic__chapter')
    
    return render(request, 'progress.html', {
        'progress': progress,
    })

def home(request):
    if request.user.is_authenticated:
        chapters = Chapter.objects.all().prefetch_related('topics').annotate(
            total_topics=Count('topics'),
            completed_topics=Count(
                'topics',
                filter=Q(topics__userprogress__user=request.user, topics__userprogress__completed=True)
            )
        )
        
        total_topics = Topic.objects.count()
        completed_topics = UserProgress.objects.filter(user=request.user, completed=True).count()
        progress_percentage = (completed_topics / total_topics * 100) if total_topics > 0 else 0
        
        recent_progress = UserProgress.objects.filter(
            user=request.user,
            completed=True
        ).select_related('topic', 'topic__chapter').order_by('-completed_at')[:5]
        
        context = {
            'chapters': chapters,
            'progress_percentage': round(progress_percentage),
            'total_topics': total_topics,
            'completed_topics': completed_topics,
            'recent_progress': recent_progress,
            'user': request.user,
            'is_authenticated': True,
        }
    else:
        # For anonymous users: general info (e.g., chapters and total topics only)
        chapters = Chapter.objects.all().prefetch_related('topics').annotate(
            total_topics=Count('topics')
        )
        total_topics = Topic.objects.count()

        context = {
            'chapters': chapters,
            'total_topics': total_topics,
            'is_authenticated': False,
        }

    return render(request, 'home.html', context)
