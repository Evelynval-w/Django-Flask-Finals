"""
Marshmallow schemas for Story serialization and validation.
"""
from marshmallow import Schema, fields, validate, post_load


class StoryCreateSchema(Schema):
    """Schema for creating a new story"""
    title = fields.String(required=True, validate=validate.Length(min=3, max=200))
    description = fields.String(load_default='')
    author_id = fields.Integer(load_default=0)
    illustration_url = fields.URL(load_default=None, allow_none=True)


class StoryUpdateSchema(Schema):
    """Schema for updating a story"""
    title = fields.String(validate=validate.Length(min=3, max=200))
    description = fields.String()
    status = fields.String(validate=validate.OneOf(['draft', 'published', 'suspended']))
    start_page_id = fields.Integer(allow_none=True)
    illustration_url = fields.URL(allow_none=True)


class StoryResponseSchema(Schema):
    """Schema for story responses"""
    id = fields.Integer()
    title = fields.String()
    description = fields.String()
    status = fields.String()
    author_id = fields.Integer()
    start_page_id = fields.Integer(allow_none=True)
    illustration_url = fields.String(allow_none=True)
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
