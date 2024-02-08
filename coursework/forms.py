from django import forms
from django.contrib.auth.models import User
from .models import Course, UserCourse
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

class UserCourseForm(forms.ModelForm):
    class Meta:
        model = UserCourse
        fields = ['user', 'course']
    
    def __init__(self, *args, user=None, **kwargs):
        super(UserCourseForm, self).__init__(*args, **kwargs)
        if user is not None:
            # Pre-select the user and make the field hidden
            self.fields['user'].initial = user
            self.fields['user'].widget = forms.HiddenInput()
            # Ensure the course field is displayed for selection
            self.fields['course'].queryset = Course.objects.all()
