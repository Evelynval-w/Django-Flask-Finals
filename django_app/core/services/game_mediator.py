"""
Mediator Pattern - GameMediator

Why Mediator?
- Decouples gameplay components (page display, choices, dice, stats)
- Provides single point of control for game flow
- Easy to add new features without modifying existing components
- Simplifies testing by isolating coordination logic
"""
import random
import uuid
from django.db.models import Count
from .api_client import get_api_client
from .game_memento import GameSession, SessionCaretaker
from gameplay.models import Play, PlaySession


class DiceRoller:
    """Component for handling random events"""
    
    @staticmethod
    def roll(sides=6):
        """Roll a dice and return the result"""
        return random.randint(1, sides)
    
    @staticmethod
    def check_success(roll, min_required):
        """Check if a roll meets the minimum requirement"""
        return roll >= min_required


class StatsTracker:
    """Component for gameplay statistics"""
    
    @staticmethod
    def record_play(story_id, ending_page_id, ending_label='', user=None, path=None):
        """Record a completed playthrough"""
        play = Play.objects.create(
            story_id=story_id,
            ending_page_id=ending_page_id,
            ending_label=ending_label,
            user=user,
            path=path or []
        )
        return play
    
    @staticmethod
    def get_story_stats(story_id):
        """Get statistics for a story"""
        plays = Play.objects.filter(story_id=story_id)
        total = plays.count()
        
        if total == 0:
            return {'total_plays': 0, 'endings': []}
        
        # Ending distribution
        endings = plays.values('ending_page_id', 'ending_label').annotate(
            count=Count('id')
        )
        
        return {
            'total_plays': total,
            'endings': [
                {
                    'ending_page_id': e['ending_page_id'],
                    'ending_label': e['ending_label'] or f"Ending {e['ending_page_id']}",
                    'count': e['count'],
                    'percentage': round(e['count'] / total * 100, 1)
                }
                for e in endings
            ]
        }


class GameMediator:
    """
    Central coordinator for all gameplay components.
    
    Usage:
        mediator = GameMediator()
        game = mediator.start_game(story_id, user)
        result = mediator.make_choice(session_key, choice_id)
    """
    
    def __init__(self):
        self.api_client = get_api_client()
        self.dice_roller = DiceRoller()
        self.stats_tracker = StatsTracker()
        self.caretaker = SessionCaretaker()
    
    def start_game(self, story_id, user=None, session_key=None):
        """
        Initialize or resume a game.
        
        Args:
            story_id: ID of the story to play
            user: Optional authenticated user
            session_key: Optional session key for resuming
            
        Returns:
            dict with story, page, session info
        """
        # Get story details
        story = self.api_client.get_story(story_id)
        
        # Check for existing session to resume
        if session_key:
            try:
                existing = self.caretaker.load_session(session_key)
                if existing and existing.story_id == story_id:
                    page = self.api_client.get_page(existing.current_page_id)
                    return {
                        'story': story,
                        'page': page,
                        'session_key': session_key,
                        'path': existing.path,
                        'resumed': True
                    }
            except PlaySession.DoesNotExist:
                pass
        
        # Start new game
        start_page = self.api_client.get_start_page(story_id)
        
        # Create new session
        new_session_key = str(uuid.uuid4())
        session = GameSession(story_id, start_page['id'])
        self.caretaker.save_session(new_session_key, session, user)
        
        return {
            'story': story,
            'page': start_page,
            'session_key': new_session_key,
            'path': [start_page['id']],
            'resumed': False
        }
    
    def make_choice(self, session_key, choice_id):
        """
        Process a player's choice.
        
        Args:
            session_key: Session identifier
            choice_id: ID of the chosen option
            
        Returns:
            dict with success status, page, and optional dice results
        """
        # Load session
        try:
            session_data = self.caretaker.load_session(session_key)
        except PlaySession.DoesNotExist:
            return {'success': False, 'error': 'Session not found'}
        
        # Get current page to find the choice
        current_page = self.api_client.get_page(session_data.current_page_id)
        
        # Find the selected choice
        choice = None
        for c in current_page.get('choices', []):
            if c['id'] == choice_id:
                choice = c
                break
        
        if not choice:
            return {'success': False, 'error': 'Invalid choice'}
        
        # Handle dice roll if required
        dice_result = None
        if choice.get('dice_required'):
            roll = self.dice_roller.roll()
            min_required = choice.get('min_roll', 1)
            success = self.dice_roller.check_success(roll, min_required)
            
            dice_result = {
                'roll': roll,
                'required': min_required,
                'success': success
            }
            
            if not success:
                return {
                    'success': False,
                    'dice_failed': True,
                    'dice_result': dice_result,
                    'page': current_page,
                    'message': f"You rolled {roll}, but needed {min_required}. Try again!"
                }
        
        # Navigate to next page
        next_page = self.api_client.get_page(choice['next_page_id'])
        
        # Update session
        session_data.add_to_path(next_page['id'])
        session_data.current_page_id = next_page['id']
        self.caretaker.update_session(session_key, session_data)
        
        result = {
            'success': True,
            'page': next_page,
            'path': session_data.path,
            'is_ending': next_page.get('is_ending', False),
            'dice_result': dice_result
        }
        
        # Record completion if ending
        if next_page.get('is_ending'):
            play = self.stats_tracker.record_play(
                story_id=session_data.story_id,
                ending_page_id=next_page['id'],
                ending_label=next_page.get('ending_label', 'The End'),
                user=session_data.user,
                path=session_data.path
            )
            result['play_id'] = play.id
            result['ending_label'] = next_page.get('ending_label', 'The End')
            
            # Clean up session
            self.caretaker.delete_session(session_key)
        
        return result
    
    def get_game_state(self, session_key):
        """Get current game state for display"""
        try:
            session_data = self.caretaker.load_session(session_key)
        except PlaySession.DoesNotExist:
            return None
        
        page = self.api_client.get_page(session_data.current_page_id)
        story = self.api_client.get_story(session_data.story_id)
        
        return {
            'story': story,
            'page': page,
            'path': session_data.path,
            'session_key': session_key
        }
    
    def get_stats(self, story_id):
        """Get gameplay statistics for a story"""
        return self.stats_tracker.get_story_stats(story_id)
