from django import forms
from django.contrib.auth.models import User
from .models import Course
from django.forms import DateInput, ModelForm

class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'image', 'syllabus', 'start_date', 'end_date']
        widgets = {
            'start_date': DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'end_date': DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }
    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)

class UserCourseForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all(), label="Select User")
    course = forms.ModelChoiceField(queryset=Course.objects.all(), label="Select Course")
