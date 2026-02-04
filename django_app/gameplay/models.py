from django.db import models
from django.contrib.auth.models import User

class Play(models.Model):
    """Records a completed playthrough"""
    story_id = models.IntegerField()  # External FK to Flask
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    ending_page_id = models.IntegerField()
    ending_label = models.CharField(max_length=100, blank=True)
    path = models.JSONField(default=list)  # List of page IDs visited
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Play #{self.id} - Story {self.story_id}"

class PlaySession(models.Model):
    """Tracks in-progress games for auto-save"""
    session_key = models.CharField(max_length=100, unique=True)
    story_id = models.IntegerField()
    current_page_id = models.IntegerField()
    path = models.JSONField(default=list)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"Session {self.session_key[:8]}... - Story {self.story_id}"
