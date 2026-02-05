from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Avg, Count
from core.services import get_api_client, GameMediator
from community.models import Rating, Comment


def story_list(request):
    """List all published stories"""
    api = get_api_client()
    
    try:
        stories = api.get_stories(status='published')
    except Exception as e:
        messages.error(request, f"Could not load stories: {e}")
        stories = []
    
    # Add ratings info
    for story in stories:
        ratings = Rating.objects.filter(story_id=story['id'])
        story['avg_rating'] = ratings.aggregate(Avg('stars'))['stars__avg'] or 0
        story['rating_count'] = ratings.count()
    
    # Search filter
    search = request.GET.get('search', '')
    if search:
        stories = [s for s in stories if search.lower() in s['title'].lower() 
                   or search.lower() in s.get('description', '').lower()]
    
    # Pagination
    paginator = Paginator(stories, 12)
    page = request.GET.get('page', 1)
    stories_page = paginator.get_page(page)
    
    return render(request, 'stories/list.html', {
        'stories': stories_page,
        'search': search
    })


def story_detail(request, story_id):
    """View story details"""
    api = get_api_client()
    mediator = GameMediator()
    
    try:
        story = api.get_story(story_id)
    except LookupError:
        messages.error(request, "Story not found")
        return redirect('stories:list')
    except Exception as e:
        messages.error(request, f"Error loading story: {e}")
        return redirect('stories:list')
    
    # Get ratings and comments
    ratings = Rating.objects.filter(story_id=story_id)
    avg_rating = ratings.aggregate(Avg('stars'))['stars__avg'] or 0
    comments = Comment.objects.filter(story_id=story_id).select_related('user')[:20]
    
    # Get stats
    stats = mediator.get_stats(story_id)
    
    # Check if user has rated
    user_rating = None
    if request.user.is_authenticated:
        user_rating = Rating.objects.filter(
            user=request.user, 
            story_id=story_id
        ).first()
    
    return render(request, 'stories/detail.html', {
        'story': story,
        'avg_rating': avg_rating,
        'rating_count': ratings.count(),
        'comments': comments,
        'stats': stats,
        'user_rating': user_rating
    })
