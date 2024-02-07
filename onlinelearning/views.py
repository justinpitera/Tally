from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from accounts.models import UserProfile
from django.contrib.auth.decorators import login_required
from assignment.models import Assignment
from coursework.models import Course
from onlinelearning.models import Module
from .forms import CustomContentForm, ModuleForm
from django.contrib.contenttypes.models import ContentType
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView


def onlinelearning_view(request):
    return render(request, 'onlinelearning/onlinelearning.html', {'page_title': 'Online Learning - Tally'})

def create_module(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    if request.method == 'POST':
        form = ModuleForm(request.POST)
        if form.is_valid():
            module = form.save(commit=False)
            module.course = course  # Set the course directly
            module.save()
            # Redirect to a new URL:
            return redirect(f'{reverse("view_course", args=[course.id])}?tab=onlinelearning')
    else:
        # Prepopulate the course field if necessary or exclude it from the form
        form = ModuleForm(initial={'course': course})
    
    return render(request, 'onlinelearning/create_module.html', {'form': form, 'course': course})

def submit_content(request, module_arg):
    if request.method == 'POST':
        form = CustomContentForm(request.POST, request.FILES, module_arg=module_arg)
        if form.is_valid():
            form.save()
            return redirect('module_view', module_arg)  # Redirect to a new URL
    else:
        form = CustomContentForm(module_arg=module_arg)
    return render(request, 'onlinelearning/submit_content.html', {'form': form})

def module_view(request, module_id):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    module = get_object_or_404(Module, pk=module_id)
    is_instructor = user_profile.role == UserProfile.INSTRUCTOR
    return render(request, 'onlinelearning/module_detail.html', {'module': module, 'is_instructor': is_instructor})
