"""
Role-based permission decorators for Django views.
"""
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden


def role_required(allowed_roles):
    """
    Decorator to require specific user roles.
    
    Usage:
        @role_required(['author', 'admin'])
        def my_view(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapped(request, *args, **kwargs):
            if not hasattr(request.user, 'profile'):
                messages.error(request, "User profile not found.")
                return redirect('stories:list')
            
            if request.user.profile.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            
            messages.error(request, "You don't have permission to access this page.")
            return redirect('stories:list')
        return wrapped
    return decorator


def author_required(view_func):
    """Shortcut decorator for author/admin access"""
    return role_required(['author', 'admin'])(view_func)


def admin_required(view_func):
    """Shortcut decorator for admin-only access"""
    return role_required(['admin'])(view_func)


def story_owner_required(view_func):
    """
    Decorator to ensure user owns the story they're editing.
    Must be used with a view that has story_id parameter.
    """
    @wraps(view_func)
    @author_required
    def wrapped(request, story_id, *args, **kwargs):
        from core.services import get_api_client
        
        api = get_api_client()
        try:
            story = api.get_story(story_id)
        except LookupError:
            messages.error(request, "Story not found.")
            return redirect('author:dashboard')
        
        # Admins can edit any story
        if request.user.profile.role == 'admin':
            return view_func(request, story_id, *args, **kwargs)
        
        # Authors can only edit their own stories
        if story.get('author_id') != request.user.id:
            messages.error(request, "You can only edit your own stories.")
            return redirect('author:dashboard')
        
        return view_func(request, story_id, *args, **kwargs)
    return wrapped
