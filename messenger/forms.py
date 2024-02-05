# forms.py
from django import forms
from .models import Message, User  # Assuming you have a Message model and User model

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['recipient', 'message'] 