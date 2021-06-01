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
            'name', 'description', 'owner_ID', 'subscribers',
        )
        widgets = {
            'name': forms.TextInput,
        }
