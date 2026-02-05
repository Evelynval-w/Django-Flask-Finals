"""
Marshmallow schemas for Page serialization and validation.
"""
from marshmallow import Schema, fields, validate


class PageCreateSchema(Schema):
    """Schema for creating a new page"""
    text = fields.String(required=True, validate=validate.Length(min=10))
    is_ending = fields.Boolean(load_default=False)
    ending_label = fields.String(load_default=None, allow_none=True)
    illustration_url = fields.URL(load_default=None, allow_none=True)


class PageUpdateSchema(Schema):
    """Schema for updating a page"""
    text = fields.String(validate=validate.Length(min=10))
    is_ending = fields.Boolean()
    ending_label = fields.String(allow_none=True)
    illustration_url = fields.URL(allow_none=True)


class PageResponseSchema(Schema):
    """Schema for page responses"""
    id = fields.Integer()
    story_id = fields.Integer()
    text = fields.String()
    is_ending = fields.Boolean()
    ending_label = fields.String(allow_none=True)
    illustration_url = fields.String(allow_none=True)
    choices = fields.List(fields.Nested('ChoiceResponseSchema'))
