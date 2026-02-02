

from app.extensions import db
from datetime import datetime

class Page(db.Model):
    __tablename__ = 'pages'
    
    id = db.Column(db.Integer, primary_key=True)
    story_id = db.Column(db.Integer, db.ForeignKey('stories.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    is_ending = db.Column(db.Boolean, default=False)
    ending_label = db.Column(db.String(100))
    illustration_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    choices = db.relationship('Choice', backref='page', lazy='dynamic', 
                             foreign_keys='Choice.page_id', cascade='all, delete-orphan')
    
    def to_dict(self, include_choices=True):
        data = {
            'id': self.id,
            'story_id': self.story_id,
            'text': self.text,
            'is_ending': self.is_ending,
            'ending_label': self.ending_label,
            'illustration_url': self.illustration_url,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        if include_choices:
            data['choices'] = [c.to_dict() for c in self.choices]
        return data
