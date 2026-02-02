

from app.extensions import db
from datetime import datetime

class Choice(db.Model):
    __tablename__ = 'choices'
    
    id = db.Column(db.Integer, primary_key=True)
    page_id = db.Column(db.Integer, db.ForeignKey('pages.id'), nullable=False)
    text = db.Column(db.String(500), nullable=False)
    next_page_id = db.Column(db.Integer, db.ForeignKey('pages.id'), nullable=True)
    dice_required = db.Column(db.Boolean, default=False)
    min_roll = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to next page
    next_page = db.relationship('Page', foreign_keys=[next_page_id])
    
    def to_dict(self):
        return {
            'id': self.id,
            'page_id': self.page_id,
            'text': self.text,
            'next_page_id': self.next_page_id,
            'dice_required': self.dice_required,
            'min_roll': self.min_roll
        }
