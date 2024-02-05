from django import forms
from django.forms import inlineformset_factory
from .models import Assignment, Attachment, Submission

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['course', 'name', 'instruction', 'start_date', 'end_date']

AttachmentFormSet = inlineformset_factory(
    Assignment, Attachment, 
    fields=['file'], extra=1, can_delete=True
)


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['file']
        widgets = {
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }