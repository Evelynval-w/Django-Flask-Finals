from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Rating(models.Model):
    """User rating for a story"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    story_id = models.IntegerField()  # External FK to Flask
    stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'story_id']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} rated Story {self.story_id}: {self.stars}★"

class Comment(models.Model):
    """User comment on a story"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    story_id = models.IntegerField()  # External FK to Flask
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} on Story {self.story_id}"

class ReportStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    REVIEWED = 'reviewed', 'Reviewed'
    RESOLVED = 'resolved', 'Resolved'
    DISMISSED = 'dismissed', 'Dismissed'

class Report(models.Model):
    """Report inappropriate content"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    story_id = models.IntegerField()  # External FK to Flask
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=ReportStatus.choices, default=ReportStatus.PENDING)
    admin_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Report #{self.id} - Story {self.story_id} ({self.status})"
