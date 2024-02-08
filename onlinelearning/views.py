from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from accounts.models import UserProfile
from django.contrib.auth.decorators import login_required
from assignment.models import Assignment
from coursework.models import Course
from onlinelearning.models import CustomContent, Module
from .forms import CustomContentForm, ModuleForm
from django.contrib.contenttypes.models import ContentType
from django.views.generic import DeleteView
from django.views.decorators.http import require_POST

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
    return render(request, 'onlinelearning/module_detail.html', {'form': form})

def module_view(request, module_id):
    # Retrieve the module object based on the provided module_id
    module = get_object_or_404(Module, pk=module_id)
    
    # Extract the associated course_id from the module
    course_id = module.course.id
    
    if request.method == 'POST':
        form = CustomContentForm(request.POST, request.FILES, module_arg=module_id)
        if form.is_valid():
            # If the form is valid, save the form and redirect
            form.save()
            # Redirect back to the module view or another view as needed
            return redirect('module_view', module_id=module_id)
    else:
        # Instantiate the form with any initial arguments if needed
        form = CustomContentForm(module_arg=module_id)
    
    # Retrieve the user profile to check if the user is an instructor
    user_profile = get_object_or_404(UserProfile, user=request.user)
    is_instructor = user_profile.role == UserProfile.INSTRUCTOR
    
    # Pass the module, course_id, form, and is_instructor flag to the template
    context = {
        'module': module,
        'course_id': course_id,  # Include the course_id in the context
        'form': form,
        'is_instructor': is_instructor
    }
    
    # Render the template with the provided context
    return render(request, 'onlinelearning/module_detail.html', context)

@login_required
@require_POST  # Ensure that this view can only be called with a POST request
def delete_custom_content(request, content_id):
    content = get_object_or_404(CustomContent, id=content_id)

    # Optional: Check if the user has the permission to delete
    if request.user != content.module.course.instructor:
        # Handle unauthorized access, e.g., show an error message or redirect
        return HttpResponseRedirect(reverse('unauthorized_access'))

    module_id = content.module.id
    content.delete()
    
    # Redirect to the module view or another success URL
    return redirect('module_view', module_id=module_id)