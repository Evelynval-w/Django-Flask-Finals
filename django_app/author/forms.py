from django import forms
from django.core.exceptions import ValidationError


class StoryForm(forms.Form):
    """Form for creating/editing stories"""
    title = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter story title'
        })
    )
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Describe your story...'
        })
    )
    illustration_url = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': 'https://example.com/image.jpg'
        })
    )
    
    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title.strip()) < 3:
            raise ValidationError("Title must be at least 3 characters")
        return title.strip()


class PageForm(forms.Form):
    """Form for creating/editing pages"""
    text = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 6,
            'placeholder': 'Write your page content here...'
        })
    )
    is_ending = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    ending_label = forms.CharField(
        required=False,
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., "The Hero Wins" or "Bad Ending"'
        })
    )
    illustration_url = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': 'https://example.com/image.jpg'
        })
    )
    
    def clean_text(self):
        text = self.cleaned_data['text']
        if len(text.strip()) < 10:
            raise ValidationError("Page text must be at least 10 characters")
        return text.strip()


class ChoiceForm(forms.Form):
    """Form for creating/editing choices"""
    text = forms.CharField(
        max_length=500,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter choice text (what the reader sees)'
        })
    )
    next_page_id = forms.IntegerField(
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    dice_required = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    min_roll = forms.IntegerField(
        required=False,
        min_value=1,
        max_value=6,
        initial=4,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '1-6'
        })
    )
    
    def __init__(self, *args, pages=None, **kwargs):
        super().__init__(*args, **kwargs)
        if pages:
            choices = [('', '-- Select target page --')]
            choices += [(p['id'], f"Page {p['id']}: {p.get('text', '')[:50]}...") for p in pages]
            self.fields['next_page_id'].widget = forms.Select(
                choices=choices,
                attrs={'class': 'form-select'}
            )


class StoryPublishForm(forms.Form):
    """Form for publishing a story"""
    confirm = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label="I confirm this story is ready for publication"
    )
