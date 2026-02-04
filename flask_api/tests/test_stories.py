import json

def test_get_stories_empty(client):
    """Test getting stories when none exist"""
    response = client.get('/stories')
    assert response.status_code == 200
    assert json.loads(response.data) == []

def test_create_story_without_api_key(client):
    """Test that creating story fails without API key"""
    response = client.post('/stories', 
        data=json.dumps({'title': 'Test'}),
        content_type='application/json')
    assert response.status_code == 401

def test_create_story_with_api_key(client, auth_headers):
    """Test creating a story with valid API key"""
    response = client.post('/stories',
        data=json.dumps({'title': 'Test Story', 'author_id': 1}),
        headers=auth_headers)
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['title'] == 'Test Story'
    assert data['status'] == 'draft'

def test_get_story(client, auth_headers):
    """Test getting a single story"""
    # Create story first
    client.post('/stories',
        data=json.dumps({'title': 'Test', 'author_id': 1}),
        headers=auth_headers)
    
    response = client.get('/stories/1')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['title'] == 'Test'
