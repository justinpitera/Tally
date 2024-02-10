from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from accounts.models import UserProfile
from django.contrib.auth.decorators import login_required
from assignment.models import Assignment, Submission
from coursework.models import Course
from onlinelearning.models import CustomContent, Module
from .forms import CustomContentForm, ModuleForm
from django.contrib.contenttypes.models import ContentType
from django.views.generic import DeleteView
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from datetime import datetime



@login_required
def onlinelearning_view(request):
    return render(request, 'onlinelearning/onlinelearning.html', {'page_title': 'Online Learning - Tally'})

@login_required
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

@login_required
def module_view(request, module_id):
    module = get_object_or_404(Module, pk=module_id)
    course = get_object_or_404(Course, id=module.course.id)
    assignments = course.assignments.prefetch_related('submissions').all()
    user_profile = get_object_or_404(UserProfile, user=request.user)
    is_instructor = user_profile.role == UserProfile.INSTRUCTOR

    assignments_submission_status = {}
    for assignment in assignments:
        submissions = assignment.submissions.filter(student=request.user)
        submission_exists = submissions.exists()
        is_late = False
        submission_count = 0

        # Check if there are submissions and if any were submitted late
        if submission_exists:
            for submission in submissions:
                # Ensure there's an end date to compare with and that the submission was late
                if assignment.end_date and submission.submitted_at.date() > assignment.end_date:
                    is_late = True
                    break  # Found a late submission, no need to check further

        # Count submissions if the user is an instructor
        if is_instructor:
            submission_count = assignment.submissions.count()

        assignments_submission_status[assignment.id] = {
            'submitted': submission_exists,
            'is_late': is_late,
            'submission_count': submission_count  # Include the submission count here
        }

    if request.method == 'POST':
        form = CustomContentForm(request.POST, request.FILES, module_arg=module_id)
        if form.is_valid():
            form.save()
            return redirect('module_view', module_id=module_id)
    else:
        form = CustomContentForm(module_arg=module_id)

    context = {
        'module': module,
        'course_id': course.id,
        'form': form,
        'is_instructor': is_instructor,
        'assignments_submission_status': assignments_submission_status,
    }

    return render(request, 'onlinelearning/view_module.html', context)



@login_required
def submit_content(request, module_arg):
    if request.method == 'POST':
        form = CustomContentForm(request.POST, request.FILES, module_arg=module_arg)
        if form.is_valid():
            form.save()
            return redirect('module_view', module_arg)  # Redirect to a new URL
    else:
        form = CustomContentForm(module_arg=module_arg)
    return render(request, 'onlinelearning/view_module.html', {'form': form})

@login_required
@require_POST  # Ensure that this view can only be called with a POST request
def delete_custom(request, content_id):
    content = get_object_or_404(CustomContent, id=content_id)

    # Optional: Check if the user has the permission to delete
    if request.user != content.module.course.instructor:
        # Handle unauthorized access, e.g., show an error message or redirect
        return HttpResponseRedirect(reverse('unauthorized_access'))

    module_id = content.module.id
    content.delete()
    
    # Redirect to the module view or another success URL
    return redirect('module_view', module_id=module_id)
