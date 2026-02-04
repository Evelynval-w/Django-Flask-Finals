"""
Memento Pattern - GameStateMemento

Why Memento?
- Preserves encapsulation of game state
- Enables save/restore without exposing internal structure
- Serializable for database storage
- Enables player path visualization
- Supports undo functionality if needed
"""
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime
import json
from gameplay.models import PlaySession


@dataclass
class GameSession:
    """
    The game state that can be saved and restored.
    Acts as the "Originator" in the Memento pattern.
    """
    story_id: int
    current_page_id: int
    path: List[int] = field(default_factory=list)
    user: Optional[object] = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def __post_init__(self):
        if not self.path:
            self.path = [self.current_page_id]
    
    def add_to_path(self, page_id: int):
        """Add a page to the player's path"""
        self.path.append(page_id)
    
    def to_dict(self):
        """Convert to dictionary for storage"""
        return {
            'story_id': self.story_id,
            'current_page_id': self.current_page_id,
            'path': self.path
        }
    
    @classmethod
    def from_dict(cls, data, user=None):
        """Create from dictionary"""
        return cls(
            story_id=data['story_id'],
            current_page_id=data['current_page_id'],
            path=data.get('path', []),
            user=user
        )


class SessionCaretaker:
    """
    Manages session storage (the "Caretaker" in Memento pattern).
    Stores mementos without knowing their internal structure.
    """
    
    def save_session(self, session_key: str, session: GameSession, user=None) -> PlaySession:
        """Save a game session to the database"""
        play_session, created = PlaySession.objects.update_or_create(
            session_key=session_key,
            defaults={
                'story_id': session.story_id,
                'current_page_id': session.current_page_id,
                'path': session.path,
                'user': user
            }
        )
        return play_session
    
    def load_session(self, session_key: str) -> GameSession:
        """Load a game session from the database"""
        play_session = PlaySession.objects.get(session_key=session_key)
        return GameSession(
            story_id=play_session.story_id,
            current_page_id=play_session.current_page_id,
            path=play_session.path,
            user=play_session.user
        )
    
    def update_session(self, session_key: str, session: GameSession):
        """Update an existing session"""
        PlaySession.objects.filter(session_key=session_key).update(
            current_page_id=session.current_page_id,
            path=session.path
        )
    
    def delete_session(self, session_key: str):
        """Delete a session (e.g., after game completion)"""
        PlaySession.objects.filter(session_key=session_key).delete()
    
    def get_user_sessions(self, user) -> List[PlaySession]:
        """Get all sessions for a user"""
        return list(PlaySession.objects.filter(user=user))
