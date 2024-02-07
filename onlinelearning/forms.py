from django import forms
from django.contrib.contenttypes.models import ContentType
from assignment.models import Assignment
from .models import CustomContent, Module
from django.db.models import Q

class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        exclude = ['course']  # Exclude course from the form
        # Alternatively, if you want to list fields explicitly, do not list 'course' here.
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'end_date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }



class CustomContentForm(forms.ModelForm):
    class Meta:
        model = CustomContent
        
        fields = ['content_type', 'file', 'url', 'urltext' ,'text', 'assignment', 'module']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'cols': 40}),            
        }

    def __init__(self, *args, **kwargs):
        module_arg = kwargs.pop('module_arg', None)  # Remove module_arg from kwargs before passing to superclass
        super(CustomContentForm, self).__init__(*args, **kwargs)
        self.fields['module'].widget = forms.HiddenInput()
        
        if module_arg is not None:
            self.fields['module'].initial = module_arg
            module_instance = Module.objects.filter(id=module_arg).first()
            if module_instance:
                # Adjust the queryset for the assignment field based on the module's course
                self.fields['assignment'].queryset = Assignment.objects.filter(course=module_instance.course)
            else:
                # If no module is found, or module_arg is not valid, clear the queryset or set a default behavior
                self.fields['assignment'].queryset = Assignment.objects.none()
