"""
Singleton Pattern - FlaskAPIClient

Why Singleton?
- Ensures single HTTP connection pool across all views
- Centralizes API key configuration
- Provides consistent error handling
- Thread-safe with locking mechanism
- Easy to mock for testing
"""
import requests
from django.conf import settings
from threading import Lock


class FlaskAPIClient:
    """
    Singleton HTTP client for Flask API communication.
    
    Usage:
        client = FlaskAPIClient()
        stories = client.get_stories()
    """
    _instance = None
    _lock = Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                # Double-check locking pattern
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Initialize the HTTP session with headers"""
        self._session = requests.Session()
        self._session.headers.update({
            'X-API-KEY': settings.FLASK_API_KEY,
            'Content-Type': 'application/json'
        })
        self._base_url = settings.FLASK_API_URL
    
    def _handle_response(self, response):
        """Centralized response handling"""
        if response.status_code == 401:
            raise PermissionError("Invalid or missing API key")
        if response.status_code == 404:
            raise LookupError("Resource not found")
        if response.status_code >= 400:
            error_msg = response.json().get('error', response.text)
            raise Exception(f"API Error: {error_msg}")
        return response.json()
    
    # ==================== STORY METHODS ====================
    
    def get_stories(self, status='published'):
        """Get all stories, optionally filtered by status"""
        response = self._session.get(
            f'{self._base_url}/stories',
            params={'status': status} if status else {}
        )
        return self._handle_response(response)
    
    def get_story(self, story_id):
        """Get a single story by ID"""
        response = self._session.get(f'{self._base_url}/stories/{story_id}')
        return self._handle_response(response)
    
    def create_story(self, data):
        """Create a new story"""
        response = self._session.post(
            f'{self._base_url}/stories',
            json=data
        )
        return self._handle_response(response)
    
    def update_story(self, story_id, data):
        """Update an existing story"""
        response = self._session.put(
            f'{self._base_url}/stories/{story_id}',
            json=data
        )
        return self._handle_response(response)
    
    def delete_story(self, story_id):
        """Delete a story"""
        response = self._session.delete(f'{self._base_url}/stories/{story_id}')
        return self._handle_response(response)
    
    def get_story_tree(self, story_id):
        """Get story structure for visualization"""
        response = self._session.get(f'{self._base_url}/stories/{story_id}/tree')
        return self._handle_response(response)
    
    # ==================== PAGE METHODS ====================
    
    def get_page(self, page_id):
        """Get a page with its choices"""
        response = self._session.get(f'{self._base_url}/pages/{page_id}')
        return self._handle_response(response)
    
    def get_start_page(self, story_id):
        """Get the starting page of a story"""
        response = self._session.get(f'{self._base_url}/stories/{story_id}/start')
        return self._handle_response(response)
    
    def create_page(self, story_id, data):
        """Create a new page in a story"""
        response = self._session.post(
            f'{self._base_url}/stories/{story_id}/pages',
            json=data
        )
        return self._handle_response(response)
    
    def update_page(self, page_id, data):
        """Update an existing page"""
        response = self._session.put(
            f'{self._base_url}/pages/{page_id}',
            json=data
        )
        return self._handle_response(response)
    
    def delete_page(self, page_id):
        """Delete a page"""
        response = self._session.delete(f'{self._base_url}/pages/{page_id}')
        return self._handle_response(response)
    
    # ==================== CHOICE METHODS ====================
    
    def create_choice(self, page_id, data):
        """Create a new choice on a page"""
        response = self._session.post(
            f'{self._base_url}/pages/{page_id}/choices',
            json=data
        )
        return self._handle_response(response)
    
    def update_choice(self, choice_id, data):
        """Update an existing choice"""
        response = self._session.put(
            f'{self._base_url}/choices/{choice_id}',
            json=data
        )
        return self._handle_response(response)
    
    def delete_choice(self, choice_id):
        """Delete a choice"""
        response = self._session.delete(f'{self._base_url}/choices/{choice_id}')
        return self._handle_response(response)


def get_api_client():
    """Convenience function to get the singleton instance"""
    return FlaskAPIClient()
