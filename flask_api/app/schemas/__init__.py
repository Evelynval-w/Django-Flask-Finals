"""
Schemas module - Request/Response serialization.
"""
from .story_schema import StoryCreateSchema, StoryUpdateSchema, StoryResponseSchema
from .page_schema import PageCreateSchema, PageUpdateSchema, PageResponseSchema
from .choice_schema import ChoiceCreateSchema, ChoiceUpdateSchema, ChoiceResponseSchema

__all__ = [
    'StoryCreateSchema',
    'StoryUpdateSchema', 
    'StoryResponseSchema',
    'PageCreateSchema',
    'PageUpdateSchema',
    'PageResponseSchema',
    'ChoiceCreateSchema',
    'ChoiceUpdateSchema',
    'ChoiceResponseSchema'
]
