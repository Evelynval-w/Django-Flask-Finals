from django import forms
from community.models import Report, ReportStatus


class ReportActionForm(forms.Form):
    """Form for admin to handle reports"""
    status = forms.ChoiceField(
        choices=ReportStatus.choices,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    admin_notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Add notes about your decision...'
        })
    )
    suspend_story = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label="Suspend the reported story"
    )


class UserRoleForm(forms.Form):
    """Form for changing user roles"""
    ROLE_CHOICES = [
        ('reader', 'Reader'),
        ('author', 'Author'),
        ('admin', 'Admin'),
    ]
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
