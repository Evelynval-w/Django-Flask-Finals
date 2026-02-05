"""
Middleware module - Request processing middleware.
"""
from .api_key_auth import require_api_key

__all__ = ['require_api_key']
