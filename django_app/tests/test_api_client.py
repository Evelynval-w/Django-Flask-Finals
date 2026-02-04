from unittest.mock import patch, MagicMock
from django.test import TestCase
from core.services import FlaskAPIClient, get_api_client

class FlaskAPIClientTest(TestCase):
    def test_singleton_instance(self):
        """Test that FlaskAPIClient is a singleton"""
        client1 = FlaskAPIClient()
        client2 = FlaskAPIClient()
        self.assertIs(client1, client2)
    
    @patch('core.services.api_client.requests.Session')
    def test_get_stories(self, mock_session):
        """Test getting stories from API"""
        # Reset singleton for clean test
        FlaskAPIClient._instance = None
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{'id': 1, 'title': 'Test'}]
        
        mock_session_instance = MagicMock()
        mock_session_instance.get.return_value = mock_response
        mock_session.return_value = mock_session_instance
        
        client = get_api_client()
        stories = client.get_stories()
        
        self.assertEqual(len(stories), 1)
        self.assertEqual(stories[0]['title'], 'Test')
