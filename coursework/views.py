from django.shortcuts import render, redirect, get_object_or_404

from assignment.models import Attachment

from .models import Course, UserCourse
from .forms import UserCourseForm, CourseForm
from django.contrib.auth.decorators import login_required
from .models import Course, UserCourse
from accounts.models import UserProfile
from django.http import FileResponse, Http404, JsonResponse
@login_required
def unenroll_user_from_course(request, course_id, user_id):
    # Ensure the request is POST for security reasons
    if request.method == 'POST':
        # Get the course, ensuring only an authorized user can unenroll participants
        course = get_object_or_404(Course, id=course_id)
        
        # Optional: Check if the request.user is the instructor of the course or has other permissions
        if course.instructor != request.user:
            # Redirect or show an error if the user is not authorized to unenroll participants from this course
            return redirect('coursework')

        # Get the UserCourse instance that links the user to the course
        user_course = get_object_or_404(UserCourse, course=course, user_id=user_id)
        
        # Remove the user from the course
        user_course.delete()
        
        # Redirect to the course detail page or another appropriate page
        return redirect('coursework')
    else:
        # If the request is not POST, redirect to a safe page; here, we use the course detail page
        return redirect('coursework')


def course_detail_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    user_profile = get_object_or_404(UserProfile, user=request.user)
    assignments = course.assignments.all()  # Assuming your Course model has a related_name='assignments'
    is_instructor = user_profile.role == UserProfile.INSTRUCTOR
    return render(request, 'coursework/view_course.html', {'course': course, 'assignments': assignments,'is_instructor': is_instructor})


@login_required  # Ensure only logged-in users can create a course
def create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)  # Save the form temporarily without committing to the database
            course.instructor = request.user  # Set the current user as the instructor
            course.save()  # Now save the course to the database
            return redirect('coursework')  # Redirect to a success page or the list of courses
    else:
        form = CourseForm()
    return render(request, 'coursework/create_course.html', {'form': form})

def add_user_to_course(request):
    if request.method == 'POST':
        form = UserCourseForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            course = form.cleaned_data['course']
            
            # Check if the user is already associated with the course
            if UserCourse.objects.filter(user=user, course=course).exists():
                # User is already in the course, so display an error message
                return redirect('coursework') #fix later!@
            else:
                # Create the association since it doesn't exist
                UserCourse.objects.create(user=user, course=course)
                # Redirect to a new URL: adjust as needed
                return redirect('coursework')
    else:
        form = UserCourseForm()
    return render(request, 'coursework/add_user_to_course.html', {'form': form})

def coursework_view(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    user_courses = UserCourse.objects.filter(user=request.user).select_related('course')
    is_instructor = user_profile.role == UserProfile.INSTRUCTOR
    return render(request, 'coursework/coursework.html', {'user_courses': user_courses,'page_title': 'Coursework - Tally','is_instructor': is_instructor})


def download_attachment(request, attachment_id):
    attachment = get_object_or_404(Attachment, id=attachment_id)
    try:
        return FileResponse(attachment.file.open(), as_attachment=True, filename=attachment.file.name)
    except FileNotFoundError:
        raise Http404('File does not exist')