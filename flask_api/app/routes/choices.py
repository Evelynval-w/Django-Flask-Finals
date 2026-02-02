

from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Choice
from app.middleware.api_key_auth import require_api_key

choices_bp = Blueprint('choices', __name__, url_prefix='/choices')

@choices_bp.route('/<int:choice_id>', methods=['GET'])
def get_choice(choice_id):
    """Get a single choice"""
    choice = Choice.query.get_or_404(choice_id)
    return jsonify(choice.to_dict())

@choices_bp.route('/<int:choice_id>', methods=['PUT'])
@require_api_key
def update_choice(choice_id):
    """Update a choice"""
    choice = Choice.query.get_or_404(choice_id)
    data = request.get_json()
    
    if 'text' in data:
        choice.text = data['text']
    if 'next_page_id' in data:
        choice.next_page_id = data['next_page_id']
    if 'dice_required' in data:
        choice.dice_required = data['dice_required']
    if 'min_roll' in data:
        choice.min_roll = data['min_roll']
    
    db.session.commit()
    return jsonify(choice.to_dict())

@choices_bp.route('/<int:choice_id>', methods=['DELETE'])
@require_api_key
def delete_choice(choice_id):
    """Delete a choice"""
    choice = Choice.query.get_or_404(choice_id)
    db.session.delete(choice)
    db.session.commit()
    return jsonify({'message': 'Choice deleted'})
