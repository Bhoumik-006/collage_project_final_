from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    event_link = forms.URLField(
        required=True,
        widget=forms.URLInput(attrs={
            'placeholder': 'https://example.com/register (Required)',
            'class': 'form-control'
        }),
        help_text='Registration link or event website is mandatory'
    )

    status = forms.ChoiceField(
        choices=Event.STATUS_CHOICES,
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control status-dropdown',
            'style': 'min-width: 200px; padding: 8px 12px; font-size: 14px; border-radius: 6px;'
        }),
        help_text='Approval status of the event'
    )
    
    class Meta:
        model = Event
        fields = ['title', 'description', 'category', 'date', 'time', 'location', 'event_flyer', 'event_link', 'status']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'description': forms.Textarea(attrs={'rows': 5}),
            'event_flyer': forms.FileInput(attrs={'accept': 'image/*', 'id': 'event-flyer'}),
        }

class DenyEventForm(forms.Form):
    denial_reason = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 5,
            'class': 'form-control',
            'style': 'min-width: 400px; min-height: 120px; padding: 12px; font-size: 14px; border-radius: 6px; border: 2px solid #dc3545;',
            'placeholder': 'Please provide a clear reason for denying this event...'
        }),
        label="Reason for Denial",
        help_text="Provide a detailed explanation that will help the organizer understand why the event was denied."
    )
