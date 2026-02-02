

from app.extensions import db
from datetime import datetime
from enum import Enum

class StoryStatus(str, Enum):
    DRAFT = 'draft'
    PUBLISHED = 'published'
    SUSPENDED = 'suspended'

class Story(db.Model):
    __tablename__ = 'stories'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default=StoryStatus.DRAFT.value)
    author_id = db.Column(db.Integer, nullable=False)
    start_page_id = db.Column(db.Integer, nullable=True)
    illustration_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    pages = db.relationship('Page', backref='story', lazy='dynamic', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'author_id': self.author_id,
            'start_page_id': self.start_page_id,
            'illustration_url': self.illustration_url,
            'page_count': self.pages.count(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
