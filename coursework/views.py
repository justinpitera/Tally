from django.shortcuts import render, redirect, get_object_or_404

from .models import Course, UserCourse
from .forms import UserCourseForm, CourseForm
from django.contrib.auth.decorators import login_required

from .models import Course, UserCourse
from django.http import JsonResponse

@login_required
def remove_user_from_course(request, user_course_id):
    if request.method == 'POST':
        user_course = get_object_or_404(UserCourse, id=user_course_id, user=request.user)
        user_course.delete()
        return JsonResponse({'status': 'success', 'message': 'Unenrolled successfully'}, status=200)
    else:
        # Handle non-POST requests or return an error
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

def course_detail_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    assignments = course.assignments.all()  # Assuming your Course model has a related_name='assignments'
    return render(request, 'coursework/view_course.html', {'course': course, 'assignments': assignments})


def create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('coursework')
    else:
        form = CourseForm()
    return render(request, 'coursework/create_course.html', {'form': form})

def add_user_to_course(request):
    if request.method == 'POST':
        form = UserCourseForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            course = form.cleaned_data['course']
            UserCourse.objects.create(user=user, course=course)  # Create the association
            return redirect('coursework')  # Redirect to a new URL: adjust as needed
    else:
        form = UserCourseForm()
    return render(request, 'coursework/add_user_to_course.html', {'form': form})

def coursework_view(request):
    user_courses = UserCourse.objects.filter(user=request.user).select_related('course')
    return render(request, 'coursework/coursework.html', {'user_courses': user_courses,'page_title': 'Coursework - Tally'})



