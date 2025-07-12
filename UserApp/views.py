from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from coreApp.models import Chapter, Topic ,User # Import from coreApp
from .models import UserProgress
from django.db.models import Count, Q
#from django.contrib.auth.models import User
from datetime import datetime, timedelta

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
    
    # Your existing topic query with is_completed annotation
    topics = chapter.topics.all().annotate(
        is_completed=Count('userprogress', filter=Q(userprogress__user=request.user, userprogress__completed=True))
    ).order_by('order', 'created_at')
    
    # Calculate chapter-level progress
    total_topics = topics.count()
    completed_topics = 0
    
    if request.user.is_authenticated:
        # Count completed topics for this user in this chapter
        completed_topics = UserProgress.objects.filter(
            user=request.user,
            topic__chapter=chapter,
            completed=True
        ).count()
    
    # Calculate remaining topics
    remaining_topics = total_topics - completed_topics
    
    # Get navigation chapters (optional)
    previous_chapter = Chapter.objects.filter(
        order__lt=chapter.order
    ).order_by('-order').first() if hasattr(chapter, 'order') else None
    
    next_chapter = Chapter.objects.filter(
        order__gt=chapter.order
    ).order_by('order').first() if hasattr(chapter, 'order') else None
    
    return render(request, 'chapter_detail.html', {
        'chapter': chapter,
        'topics': topics,
        'completed_topics': completed_topics,
        'total_topics': total_topics,
        'remaining_topics': remaining_topics,
        'previous_chapter': previous_chapter,
        'next_chapter': next_chapter,
    })
def topic_detail(request, pk):
    topic = get_object_or_404(Topic, pk=pk)
    
    # Get previous and next topics within the same chapter
    previous_topic = Topic.objects.filter(
        chapter=topic.chapter,
        order__lt=topic.order
    ).order_by('-order').first()
    
    next_topic = Topic.objects.filter(
        chapter=topic.chapter,
        order__gt=topic.order
    ).order_by('order').first()
    
    # Check if topic is completed
    is_completed = UserProgress.objects.filter(
        user=request.user, topic=topic, completed=True
    ).exists()
    
    # Calculate chapter progress
    chapter_topics = Topic.objects.filter(chapter=topic.chapter).order_by('order')
    current_position = list(chapter_topics).index(topic) + 1
    total_topics = chapter_topics.count()
    progress_percentage = (current_position / total_topics) * 100
    
    return render(request, 'topic_detail.html', {
        'topic': topic,
        'is_completed': is_completed,
        'previous_topic': previous_topic,
        'next_topic': next_topic,
        'current_position': current_position,
        'total_topics': total_topics,
        'progress_percentage': progress_percentage,
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
    # Calculate global statistics for all users
    total_topics = Topic.objects.count()
    total_users = User.objects.count()
    total_chapters = Chapter.objects.count()
    
    # Calculate success rate (users who completed at least one topic)
    users_with_progress = User.objects.filter(
        userprogress__completed=True
    ).distinct().count()
    
    success_rate = 0
    if total_users > 0:
        success_rate = round((users_with_progress / total_users) * 100)
    
    # Additional statistics
    total_completions = UserProgress.objects.filter(completed=True).count()
    
    # Recent activity (last 7 days)
    week_ago = datetime.now() - timedelta(days=7)
    recent_completions = UserProgress.objects.filter(
        completed=True,
        completed_at__gte=week_ago
    ).count()

    if request.user.is_authenticated:
        chapters = Chapter.objects.all().prefetch_related('topics').annotate(
            total_topics=Count('topics'),
            completed_topics=Count(
                'topics',
                filter=Q(topics__userprogress__user=request.user, topics__userprogress__completed=True)
            )
        )
        
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
            # Global statistics
            'total_users': total_users,
            'total_chapters': total_chapters,
            'success_rate': success_rate,
            'total_completions': total_completions,
            'recent_completions': recent_completions,
        }
    else:
        # For anonymous users
        chapters = Chapter.objects.all().prefetch_related('topics').annotate(
            total_topics=Count('topics')
        )
        
        context = {
            'chapters': chapters,
            'total_topics': total_topics,
            'is_authenticated': False,
            # Global statistics
            'total_users': total_users,
            'total_chapters': total_chapters,
            'success_rate': success_rate,
            'total_completions': total_completions,
            'recent_completions': recent_completions,
        }
    
    return render(request, 'home.html', context)
