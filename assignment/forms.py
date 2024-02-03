from django import forms
from django.forms import inlineformset_factory
from .models import Assignment, Attachment

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['course', 'name', 'instruction', 'start_date', 'end_date']

AttachmentFormSet = inlineformset_factory(
    Assignment, Attachment, 
    fields=['file'], extra=1, can_delete=True
)
