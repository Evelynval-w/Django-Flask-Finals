from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.services import get_api_client, StoryFactory
from core.middleware import author_required, story_owner_required
from .forms import StoryForm, PageForm, ChoiceForm, StoryPublishForm


@author_required
def dashboard(request):
    """Author dashboard - list own stories"""
    api = get_api_client()
    
    try:
        all_stories = api.get_stories(status=None)
        my_stories = [s for s in all_stories if s.get('author_id') == request.user.id]
    except Exception as e:
        messages.error(request, f"Could not load stories: {e}")
        my_stories = []
    
    drafts = [s for s in my_stories if s['status'] == 'draft']
    published = [s for s in my_stories if s['status'] == 'published']
    suspended = [s for s in my_stories if s['status'] == 'suspended']
    
    return render(request, 'author/dashboard.html', {
        'drafts': drafts,
        'published': published,
        'suspended': suspended
    })


@author_required
def create_story(request):
    """Create a new story"""
    if request.method == 'POST':
        form = StoryForm(request.POST)
        if form.is_valid():
            api = get_api_client()
            try:
                story_data = StoryFactory.create_story(
                    title=form.cleaned_data['title'],
                    description=form.cleaned_data['description'],
                    author_id=request.user.id,
                    illustration_url=form.cleaned_data.get('illustration_url')
                )
                story = api.create_story(story_data)
                messages.success(request, f"Story '{story['title']}' created!")
                return redirect('author:edit_story', story_id=story['id'])
            except Exception as e:
                messages.error(request, f"Error creating story: {e}")
    else:
        form = StoryForm()
    
    return render(request, 'author/story_form.html', {'form': form, 'action': 'Create'})


@story_owner_required
def edit_story(request, story_id):
    """Edit story details and manage pages"""
    api = get_api_client()
    
    try:
        story = api.get_story(story_id)
        tree = api.get_story_tree(story_id)
    except Exception as e:
        messages.error(request, f"Error loading story: {e}")
        return redirect('author:dashboard')
    
    if request.method == 'POST':
        form = StoryForm(request.POST)
        if form.is_valid():
            try:
                api.update_story(story_id, {
                    'title': form.cleaned_data['title'],
                    'description': form.cleaned_data['description'],
                    'illustration_url': form.cleaned_data.get('illustration_url')
                })
                messages.success(request, "Story updated!")
                return redirect('author:edit_story', story_id=story_id)
            except Exception as e:
                messages.error(request, f"Error updating story: {e}")
    else:
        form = StoryForm(initial={
            'title': story['title'],
            'description': story.get('description', ''),
            'illustration_url': story.get('illustration_url', '')
        })
    
    return render(request, 'author/edit_story.html', {'form': form, 'story': story, 'tree': tree})


@story_owner_required
def add_page(request, story_id):
    """Add a new page to story"""
    api = get_api_client()
    
    try:
        story = api.get_story(story_id)
    except Exception as e:
        messages.error(request, f"Error loading story: {e}")
        return redirect('author:dashboard')
    
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            try:
                page_data = StoryFactory.create_page(
                    story_id=story_id,
                    text=form.cleaned_data['text'],
                    is_ending=form.cleaned_data.get('is_ending', False),
                    ending_label=form.cleaned_data.get('ending_label'),
                    illustration_url=form.cleaned_data.get('illustration_url')
                )
                page = api.create_page(story_id, page_data)
                messages.success(request, f"Page {page['id']} created!")
                return redirect('author:edit_page', story_id=story_id, page_id=page['id'])
            except Exception as e:
                messages.error(request, f"Error creating page: {e}")
    else:
        form = PageForm()
    
    return render(request, 'author/page_form.html', {'form': form, 'story': story, 'action': 'Add'})


@story_owner_required
def edit_page(request, story_id, page_id):
    """Edit a page and manage its choices"""
    api = get_api_client()
    
    try:
        story = api.get_story(story_id)
        page = api.get_page(page_id)
        tree = api.get_story_tree(story_id)
    except Exception as e:
        messages.error(request, f"Error loading page: {e}")
        return redirect('author:edit_story', story_id=story_id)
    
    all_pages = [n for n in tree['nodes']]
    
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            try:
                api.update_page(page_id, {
                    'text': form.cleaned_data['text'],
                    'is_ending': form.cleaned_data.get('is_ending', False),
                    'ending_label': form.cleaned_data.get('ending_label'),
                    'illustration_url': form.cleaned_data.get('illustration_url')
                })
                messages.success(request, "Page updated!")
                return redirect('author:edit_page', story_id=story_id, page_id=page_id)
            except Exception as e:
                messages.error(request, f"Error updating page: {e}")
    else:
        form = PageForm(initial={
            'text': page['text'],
            'is_ending': page.get('is_ending', False),
            'ending_label': page.get('ending_label', ''),
            'illustration_url': page.get('illustration_url', '')
        })
    
    choice_form = ChoiceForm(pages=all_pages)
    
    return render(request, 'author/edit_page.html', {
        'form': form, 'choice_form': choice_form, 'story': story, 'page': page, 'all_pages': all_pages
    })


@story_owner_required
def add_choice(request, story_id, page_id):
    """Add a choice to a page"""
    if request.method != 'POST':
        return redirect('author:edit_page', story_id=story_id, page_id=page_id)
    
    api = get_api_client()
    try:
        tree = api.get_story_tree(story_id)
        all_pages = [n for n in tree['nodes']]
    except:
        all_pages = []
    
    form = ChoiceForm(request.POST, pages=all_pages)
    if form.is_valid():
        try:
            choice_data = StoryFactory.create_choice(
                page_id=page_id,
                text=form.cleaned_data['text'],
                next_page_id=form.cleaned_data.get('next_page_id'),
                dice_required=form.cleaned_data.get('dice_required', False),
                min_roll=form.cleaned_data.get('min_roll')
            )
            api.create_choice(page_id, choice_data)
            messages.success(request, "Choice added!")
        except Exception as e:
            messages.error(request, f"Error adding choice: {e}")
    
    return redirect('author:edit_page', story_id=story_id, page_id=page_id)


@story_owner_required
def delete_choice(request, story_id, page_id, choice_id):
    """Delete a choice"""
    if request.method == 'POST':
        api = get_api_client()
        try:
            api.delete_choice(choice_id)
            messages.success(request, "Choice deleted!")
        except Exception as e:
            messages.error(request, f"Error deleting choice: {e}")
    return redirect('author:edit_page', story_id=story_id, page_id=page_id)


@story_owner_required
def delete_page(request, story_id, page_id):
    """Delete a page"""
    if request.method == 'POST':
        api = get_api_client()
        try:
            api.delete_page(page_id)
            messages.success(request, "Page deleted!")
        except Exception as e:
            messages.error(request, f"Error deleting page: {e}")
    return redirect('author:edit_story', story_id=story_id)


@story_owner_required
def publish_story(request, story_id):
    """Publish a story"""
    api = get_api_client()
    
    try:
        story = api.get_story(story_id)
        tree = api.get_story_tree(story_id)
    except Exception as e:
        messages.error(request, f"Error loading story: {e}")
        return redirect('author:dashboard')
    
    errors = []
    if len(tree['nodes']) < 2:
        errors.append("Story must have at least 2 pages")
    endings = [n for n in tree['nodes'] if n.get('is_ending')]
    if not endings:
        errors.append("Story must have at least one ending page")
    if not story.get('start_page_id'):
        errors.append("Story must have a start page")
    
    if request.method == 'POST' and not errors:
        form = StoryPublishForm(request.POST)
        if form.is_valid():
            try:
                api.update_story(story_id, {'status': 'published'})
                messages.success(request, f"'{story['title']}' is now published!")
                return redirect('author:dashboard')
            except Exception as e:
                messages.error(request, f"Error publishing: {e}")
    else:
        form = StoryPublishForm()
    
    return render(request, 'author/publish.html', {'form': form, 'story': story, 'tree': tree, 'errors': errors})


@story_owner_required
def set_start_page(request, story_id, page_id):
    """Set a page as the story's start page"""
    if request.method == 'POST':
        api = get_api_client()
        try:
            api.update_story(story_id, {'start_page_id': page_id})
            messages.success(request, f"Page {page_id} set as start page!")
        except Exception as e:
            messages.error(request, f"Error: {e}")
    return redirect('author:edit_story', story_id=story_id)


@story_owner_required  
def delete_story(request, story_id):
    """Delete a story"""
    if request.method == 'POST':
        api = get_api_client()
        try:
            api.delete_story(story_id)
            messages.success(request, "Story deleted!")
        except Exception as e:
            messages.error(request, f"Error deleting story: {e}")
    return redirect('author:dashboard')


@story_owner_required
def preview_story(request, story_id):
    """Preview story"""
    api = get_api_client()
    try:
        story = api.get_story(story_id)
        start_page = api.get_start_page(story_id)
    except Exception as e:
        messages.error(request, f"Error: {e}")
        return redirect('author:edit_story', story_id=story_id)
    return render(request, 'author/preview.html', {'story': story, 'page': start_page, 'is_preview': True})
