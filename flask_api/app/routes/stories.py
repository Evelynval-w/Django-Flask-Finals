

from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Story, StoryStatus, Page
from app.middleware.api_key_auth import require_api_key

stories_bp = Blueprint('stories', __name__, url_prefix='/stories')

@stories_bp.route('', methods=['GET'])
def get_stories():
    """Get all stories, optionally filtered by status"""
    status = request.args.get('status', 'published')
    
    query = Story.query
    if status:
        query = query.filter_by(status=status)
    
    stories = query.order_by(Story.created_at.desc()).all()
    return jsonify([s.to_dict() for s in stories])

@stories_bp.route('/<int:story_id>', methods=['GET'])
def get_story(story_id):
    """Get a single story by ID"""
    story = Story.query.get_or_404(story_id)
    return jsonify(story.to_dict())

@stories_bp.route('/<int:story_id>/start', methods=['GET'])
def get_start_page(story_id):
    """Get the starting page of a story"""
    story = Story.query.get_or_404(story_id)
    
    if not story.start_page_id:
        # Return first page if no start page set
        first_page = Page.query.filter_by(story_id=story_id).first()
        if not first_page:
            return jsonify({'error': 'Story has no pages'}), 404
        return jsonify(first_page.to_dict())
    
    start_page = Page.query.get_or_404(story.start_page_id)
    return jsonify(start_page.to_dict())

@stories_bp.route('/<int:story_id>/tree', methods=['GET'])
def get_story_tree(story_id):
    """Get story structure for visualization"""
    story = Story.query.get_or_404(story_id)
    pages = Page.query.filter_by(story_id=story_id).all()
    
    nodes = []
    edges = []
    
    for page in pages:
        nodes.append({
            'id': page.id,
            'label': f'Page {page.id}',
            'is_start': page.id == story.start_page_id,
            'is_ending': page.is_ending,
            'ending_label': page.ending_label
        })
        
        for choice in page.choices:
            if choice.next_page_id:
                edges.append({
                    'source': page.id,
                    'target': choice.next_page_id,
                    'label': choice.text[:30] + '...' if len(choice.text) > 30 else choice.text
                })
    
    return jsonify({'nodes': nodes, 'edges': edges})

@stories_bp.route('', methods=['POST'])
@require_api_key
def create_story():
    """Create a new story"""
    data = request.get_json()
    
    if not data.get('title'):
        return jsonify({'error': 'Title is required'}), 400
    
    story = Story(
        title=data['title'],
        description=data.get('description', ''),
        author_id=data.get('author_id', 0),
        status=StoryStatus.DRAFT.value
    )
    
    db.session.add(story)
    db.session.commit()
    
    return jsonify(story.to_dict()), 201

@stories_bp.route('/<int:story_id>', methods=['PUT'])
@require_api_key
def update_story(story_id):
    """Update a story"""
    story = Story.query.get_or_404(story_id)
    data = request.get_json()
    
    if 'title' in data:
        story.title = data['title']
    if 'description' in data:
        story.description = data['description']
    if 'status' in data:
        story.status = data['status']
    if 'start_page_id' in data:
        story.start_page_id = data['start_page_id']
    if 'illustration_url' in data:
        story.illustration_url = data['illustration_url']
    
    db.session.commit()
    return jsonify(story.to_dict())

@stories_bp.route('/<int:story_id>', methods=['DELETE'])
@require_api_key
def delete_story(story_id):
    """Delete a story and all its pages/choices"""
    story = Story.query.get_or_404(story_id)
    db.session.delete(story)
    db.session.commit()
    return jsonify({'message': 'Story deleted'}), 200

@stories_bp.route('/<int:story_id>/pages', methods=['POST'])
@require_api_key
def create_page(story_id):
    """Add a page to a story"""
    story = Story.query.get_or_404(story_id)
    data = request.get_json()
    
    if not data.get('text'):
        return jsonify({'error': 'Page text is required'}), 400
    
    page = Page(
        story_id=story_id,
        text=data['text'],
        is_ending=data.get('is_ending', False),
        ending_label=data.get('ending_label'),
        illustration_url=data.get('illustration_url')
    )
    
    db.session.add(page)
    db.session.commit()
    
    # Set as start page if it's the first page
    if story.pages.count() == 1:
        story.start_page_id = page.id
        db.session.commit()
    
    return jsonify(page.to_dict()), 201
