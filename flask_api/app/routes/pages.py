
from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Page, Choice
from app.middleware.api_key_auth import require_api_key

pages_bp = Blueprint('pages', __name__, url_prefix='/pages')

@pages_bp.route('/<int:page_id>', methods=['GET'])
def get_page(page_id):
    """Get a page with its choices"""
    page = Page.query.get_or_404(page_id)
    return jsonify(page.to_dict())

@pages_bp.route('/<int:page_id>', methods=['PUT'])
@require_api_key
def update_page(page_id):
    """Update a page"""
    page = Page.query.get_or_404(page_id)
    data = request.get_json()
    
    if 'text' in data:
        page.text = data['text']
    if 'is_ending' in data:
        page.is_ending = data['is_ending']
    if 'ending_label' in data:
        page.ending_label = data['ending_label']
    if 'illustration_url' in data:
        page.illustration_url = data['illustration_url']
    
    db.session.commit()
    return jsonify(page.to_dict())

@pages_bp.route('/<int:page_id>', methods=['DELETE'])
@require_api_key
def delete_page(page_id):
    """Delete a page"""
    page = Page.query.get_or_404(page_id)
    db.session.delete(page)
    db.session.commit()
    return jsonify({'message': 'Page deleted'})

@pages_bp.route('/<int:page_id>/choices', methods=['POST'])
@require_api_key
def create_choice(page_id):
    """Add a choice to a page"""
    page = Page.query.get_or_404(page_id)
    data = request.get_json()
    
    if not data.get('text'):
        return jsonify({'error': 'Choice text is required'}), 400
    
    choice = Choice(
        page_id=page_id,
        text=data['text'],
        next_page_id=data.get('next_page_id'),
        dice_required=data.get('dice_required', False),
        min_roll=data.get('min_roll', 1)
    )
    
    db.session.add(choice)
    db.session.commit()
    
    return jsonify(choice.to_dict()), 201
