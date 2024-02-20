# forms.py
from django import forms
from .models import Message
from django.contrib.auth.models import User

class MessageForm(forms.ModelForm):
    recipient = forms.ModelChoiceField(queryset=User.objects.all(), empty_label="Select Recipient")

    class Meta:
        model = Message
        fields = ['recipient', 'subject', 'content' ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Extract the user from kwargs
        super(MessageForm, self).__init__(*args, **kwargs)
        if self.user:  # Filter the queryset to exclude the current user
            self.fields['recipient'].queryset = User.objects.exclude(id=self.user.id)

class DirectMessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content','subject'] 

