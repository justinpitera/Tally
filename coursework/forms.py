from django import forms
from django.contrib.auth.models import User
from .models import Course
from django.forms import ModelForm

class CourseForm(ModelForm):
    # Optionally, add instructor here explicitly if you want to customize it further,
    # e.g., to change the label or help_text.
    # instructor = forms.ModelChoiceField(queryset=User.objects.none(), required=True, label="Instructor")

    class Meta:
        model = Course
        fields = ['title','description','image','syllabus','start_date', 'end_date']

    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)
        # Set the queryset for instructor field to all User objects.
        # This populates the dropdown for the instructor field with all users.

        # If you've explicitly added the instructor field above, you might not need to set queryset here again,
        # unless you're filtering the queryset based on some criteria.


class UserCourseForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all(), label="Select User")
    course = forms.ModelChoiceField(queryset=Course.objects.all(), label="Select Course")
