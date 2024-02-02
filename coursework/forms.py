from django import forms
from django.contrib.auth.models import User
from .models import Course
from django.forms import ModelForm

class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'instructor', 'start_date', 'end_date', 'image']


class UserCourseForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all(), label="Select User")
    course = forms.ModelChoiceField(queryset=Course.objects.all(), label="Select Course")
