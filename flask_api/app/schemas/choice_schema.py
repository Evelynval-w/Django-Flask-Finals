"""
Marshmallow schemas for Choice serialization and validation.
"""
from marshmallow import Schema, fields, validate


class ChoiceCreateSchema(Schema):
    """Schema for creating a new choice"""
    text = fields.String(required=True, validate=validate.Length(min=2, max=500))
    next_page_id = fields.Integer(load_default=None, allow_none=True)
    dice_required = fields.Boolean(load_default=False)
    min_roll = fields.Integer(load_default=1, validate=validate.Range(min=1, max=6))


class ChoiceUpdateSchema(Schema):
    """Schema for updating a choice"""
    text = fields.String(validate=validate.Length(min=2, max=500))
    next_page_id = fields.Integer(allow_none=True)
    dice_required = fields.Boolean()
    min_roll = fields.Integer(validate=validate.Range(min=1, max=6))


class ChoiceResponseSchema(Schema):
    """Schema for choice responses"""
    id = fields.Integer()
    page_id = fields.Integer()
    text = fields.String()
    next_page_id = fields.Integer(allow_none=True)
    dice_required = fields.Boolean()
    min_roll = fields.Integer()
