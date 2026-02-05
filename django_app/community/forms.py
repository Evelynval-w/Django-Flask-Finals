from django import forms
from .models import Rating, Comment, Report


class RatingForm(forms.Form):
    """Form for rating a story"""
    stars = forms.ChoiceField(
        choices=[(i, f"{i} Star{'s' if i > 1 else ''}") for i in range(1, 6)],
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'})
    )


class CommentForm(forms.ModelForm):
    """Form for commenting on a story"""
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Share your thoughts about this story...'
            })
        }


class ReportForm(forms.ModelForm):
    """Form for reporting inappropriate content"""
    class Meta:
        model = Report
        fields = ['reason']
        widgets = {
            'reason': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Please describe why you are reporting this story...'
            })
        }
        labels = {
            'reason': 'Reason for Report'
        }
