from django import forms
from django.forms import HiddenInput, inlineformset_factory
from .models import Assignment, Attachment, Submission
from django.forms import DateInput
class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['course', 'name', 'instruction', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'end_date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }

    def __init__(self, *args, **kwargs):
        # Extract the course_id from kwargs if it exists
        course_id = kwargs.pop('course_id', None)
        
        super(AssignmentForm, self).__init__(*args, **kwargs)  # Ensure any extra kwargs are passed to super
        # Now, safely use course_id without affecting the superclass initialization
        if course_id is not None:
            self.fields['course'].initial = course_id
            self.fields['course'].widget = HiddenInput()

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

class GradeForm(forms.ModelForm):
    class Meta:
        model = Submission 
        fields = ['grade', 'comments']


class GradeSubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['grade', 'comments']
        widgets = {
            'comments': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }


# forms.py
from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['message','file']
