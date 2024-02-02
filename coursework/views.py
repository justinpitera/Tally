from django.shortcuts import render, redirect
from .models import Course, UserCourse
from .forms import UserCourseForm, CourseForm


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