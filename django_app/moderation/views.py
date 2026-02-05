from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from core.middleware import admin_required
from core.services import get_api_client
from community.models import Report, ReportStatus
from accounts.models import UserProfile
from .forms import ReportActionForm, UserRoleForm


@admin_required
def dashboard(request):
    """Admin dashboard"""
    pending_reports = Report.objects.filter(status=ReportStatus.PENDING).count()
    total_users = User.objects.count()
    
    api = get_api_client()
    try:
        all_stories = api.get_stories(status=None)
        total_stories = len(all_stories)
        suspended_stories = len([s for s in all_stories if s['status'] == 'suspended'])
    except:
        total_stories = 0
        suspended_stories = 0
    
    return render(request, 'moderation/dashboard.html', {
        'pending_reports': pending_reports,
        'total_users': total_users,
        'total_stories': total_stories,
        'suspended_stories': suspended_stories
    })


@admin_required
def report_list(request):
    """List all reports"""
    status_filter = request.GET.get('status', '')
    reports = Report.objects.select_related('user').order_by('-created_at')
    if status_filter:
        reports = reports.filter(status=status_filter)
    return render(request, 'moderation/report_list.html', {
        'reports': reports, 'status_filter': status_filter, 'statuses': ReportStatus.choices
    })


@admin_required
def report_detail(request, report_id):
    """View and handle a report"""
    report = get_object_or_404(Report, id=report_id)
    api = get_api_client()
    try:
        story = api.get_story(report.story_id)
    except:
        story = None
    
    if request.method == 'POST':
        form = ReportActionForm(request.POST)
        if form.is_valid():
            report.status = form.cleaned_data['status']
            report.admin_notes = form.cleaned_data['admin_notes']
            report.save()
            if form.cleaned_data.get('suspend_story') and story:
                try:
                    api.update_story(report.story_id, {'status': 'suspended'})
                    messages.warning(request, f"Story '{story['title']}' has been suspended")
                except Exception as e:
                    messages.error(request, f"Could not suspend story: {e}")
            messages.success(request, "Report updated")
            return redirect('moderation:report_list')
    else:
        form = ReportActionForm(initial={'status': report.status, 'admin_notes': report.admin_notes})
    return render(request, 'moderation/report_detail.html', {'report': report, 'story': story, 'form': form})


@admin_required
def user_list(request):
    """List all users"""
    users = User.objects.select_related('profile').order_by('-date_joined')
    return render(request, 'moderation/user_list.html', {'users': users})


@admin_required
def user_detail(request, user_id):
    """View and edit user"""
    user = get_object_or_404(User, id=user_id)
    profile, _ = UserProfile.objects.get_or_create(user=user)
    if request.method == 'POST':
        form = UserRoleForm(request.POST)
        if form.is_valid():
            profile.role = form.cleaned_data['role']
            profile.save()
            messages.success(request, f"Updated {user.username}'s role to {profile.role}")
            return redirect('moderation:user_list')
    else:
        form = UserRoleForm(initial={'role': profile.role})
    return render(request, 'moderation/user_detail.html', {'target_user': user, 'profile': profile, 'form': form})


@admin_required
def story_list(request):
    """List all stories for moderation"""
    api = get_api_client()
    status_filter = request.GET.get('status', '')
    try:
        stories = api.get_stories(status=status_filter if status_filter else None)
    except:
        stories = []
    return render(request, 'moderation/story_list.html', {'stories': stories, 'status_filter': status_filter})


@admin_required
def suspend_story(request, story_id):
    """Suspend a story"""
    if request.method == 'POST':
        api = get_api_client()
        try:
            api.update_story(story_id, {'status': 'suspended'})
            messages.success(request, "Story suspended")
        except Exception as e:
            messages.error(request, f"Error: {e}")
    return redirect('moderation:story_list')


@admin_required
def unsuspend_story(request, story_id):
    """Unsuspend a story"""
    if request.method == 'POST':
        api = get_api_client()
        try:
            api.update_story(story_id, {'status': 'published'})
            messages.success(request, "Story restored to published")
        except Exception as e:
            messages.error(request, f"Error: {e}")
    return redirect('moderation:story_list')
