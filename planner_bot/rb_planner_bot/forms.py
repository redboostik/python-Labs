from django import forms
from jsonfield.fields import JSONFormField
from .models import *


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'name', 'telegram_id',
        )
        widgets = {
            'name': forms.TextInput,
        }


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = (
            'name', 'description', 'date', 'owner_ID', 'subscribers',
        )
        widgets = {
            'name': forms.TextInput,
        }


class ActiveEventsForm(forms.ModelForm):
    class Meta:
        model = ActiveEvents
        fields = (
            'event_ID', 'owner_ID',
        )


class ActiveCommandForm(forms.ModelForm):
    class Meta:
        model = ActiveCommand
        fields = (
            'user_ID', 'command',
        )


class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notifications
        fields = (
            'title', 'event_ID', 'owner_ID', 'date',
        )
