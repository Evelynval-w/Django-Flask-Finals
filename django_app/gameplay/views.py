from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from core.services import GameMediator, get_api_client
from .models import PlaySession
import json


def play_story(request, story_id):
    """Start or resume playing a story"""
    mediator = GameMediator()
    
    session_key = request.session.get(f'game_session_{story_id}')
    user = request.user if request.user.is_authenticated else None
    
    try:
        game_data = mediator.start_game(story_id, user=user, session_key=session_key)
    except LookupError:
        messages.error(request, "Story not found")
        return redirect('stories:list')
    except Exception as e:
        messages.error(request, f"Error starting game: {e}")
        return redirect('stories:list')
    
    request.session[f'game_session_{story_id}'] = game_data['session_key']
    
    if game_data.get('resumed'):
        messages.info(request, "Resuming your saved game...")
    
    return render(request, 'gameplay/play.html', {
        'story': game_data['story'],
        'page': game_data['page'],
        'session_key': game_data['session_key'],
        'path': game_data['path']
    })


def make_choice(request, story_id):
    """Process a player's choice (AJAX endpoint)"""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    
    try:
        data = json.loads(request.body)
        choice_id = data.get('choice_id')
        session_key = data.get('session_key')
    except:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    if not choice_id or not session_key:
        return JsonResponse({'error': 'Missing choice_id or session_key'}, status=400)
    
    mediator = GameMediator()
    result = mediator.make_choice(session_key, int(choice_id))
    
    if result.get('is_ending'):
        if f'game_session_{story_id}' in request.session:
            del request.session[f'game_session_{story_id}']
    
    return JsonResponse(result)


def game_state(request, story_id):
    """Get current game state (AJAX endpoint)"""
    session_key = request.session.get(f'game_session_{story_id}')
    
    if not session_key:
        return JsonResponse({'error': 'No active session'}, status=404)
    
    mediator = GameMediator()
    state = mediator.get_game_state(session_key)
    
    if not state:
        return JsonResponse({'error': 'Session not found'}, status=404)
    
    return JsonResponse(state)


def restart_game(request, story_id):
    """Restart a game from the beginning"""
    session_key = f'game_session_{story_id}'
    if session_key in request.session:
        del request.session[session_key]
    
    messages.info(request, "Starting fresh...")
    return redirect('gameplay:play', story_id=story_id)


def story_tree_data(request, story_id):
    """Get story tree data for visualization (AJAX endpoint)"""
    api = get_api_client()
    
    try:
        tree = api.get_story_tree(story_id)
        return JsonResponse(tree)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
