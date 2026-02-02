

from functools import wraps
from flask import request, jsonify, current_app

def require_api_key(f):
    """Decorator to require API key for write operations"""
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get('X-API-KEY')
        
        if not api_key:
            return jsonify({'error': 'API key required', 'code': 'MISSING_API_KEY'}), 401
        
        if api_key != current_app.config['API_KEY']:
            return jsonify({'error': 'Invalid API key', 'code': 'INVALID_API_KEY'}), 401
        
        return f(*args, **kwargs)
    return decorated
