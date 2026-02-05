from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Rating, Comment, Report
from .forms import RatingForm, CommentForm, ReportForm


@login_required
def rate_story(request, story_id):
    """Rate a story"""
    if request.method != 'POST':
        return redirect('stories:detail', story_id=story_id)
    
    form = RatingForm(request.POST)
    if form.is_valid():
        stars = int(form.cleaned_data['stars'])
        
        rating, created = Rating.objects.update_or_create(
            user=request.user,
            story_id=story_id,
            defaults={'stars': stars}
        )
        
        if created:
            messages.success(request, f"Thanks for rating! You gave {stars} stars.")
        else:
            messages.success(request, f"Rating updated to {stars} stars.")
    
    return redirect('stories:detail', story_id=story_id)


@login_required
def add_comment(request, story_id):
    """Add a comment to a story"""
    if request.method != 'POST':
        return redirect('stories:detail', story_id=story_id)
    
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.story_id = story_id
        comment.save()
        messages.success(request, "Comment added!")
    else:
        messages.error(request, "Could not add comment")
    
    return redirect('stories:detail', story_id=story_id)


@login_required
def delete_comment(request, comment_id):
    """Delete own comment"""
    try:
        comment = Comment.objects.get(id=comment_id, user=request.user)
        story_id = comment.story_id
        comment.delete()
        messages.success(request, "Comment deleted")
        return redirect('stories:detail', story_id=story_id)
    except Comment.DoesNotExist:
        messages.error(request, "Comment not found")
        return redirect('stories:list')


@login_required
def report_story(request, story_id):
    """Report a story"""
    existing = Report.objects.filter(user=request.user, story_id=story_id).first()
    if existing:
        messages.warning(request, "You have already reported this story")
        return redirect('stories:detail', story_id=story_id)
    
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.user = request.user
            report.story_id = story_id
            report.save()
            messages.success(request, "Report submitted. Thank you!")
            return redirect('stories:detail', story_id=story_id)
    else:
        form = ReportForm()
    
    return render(request, 'community/report_form.html', {
        'form': form,
        'story_id': story_id
    })
