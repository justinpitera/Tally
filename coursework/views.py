from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from assignment.forms import AssignmentForm, AttachmentFormSet
from assignment.models import Assignment, Attachment, Submission
from .models import Course, UserCourse
from .forms import UserCourseForm, CourseForm
from django.contrib.auth.decorators import login_required
from accounts.models import UserProfile
from django.http import FileResponse, Http404, JsonResponse
from django.db.models import Avg
from django.utils.timezone import now
@login_required
def direct_unenroll(request, course_id, user_id):
    # Ensure the request is POST for security reasons
    if request.method == "POST":
        # Get the course, ensuring only an authorized user can unenroll participants
        course = get_object_or_404(Course, id=course_id)

        # Get the UserCourse instance that links the user to the course
        user_course = get_object_or_404(UserCourse, course=course, user_id=user_id)

        # Remove the user from the course
        user_course.delete()

        # Redirect to the course detail page or another appropriate page
        return redirect("coursework")
    else:
        # If the request is not POST, redirect to a safe page; here, we use the course detail page
        return redirect("coursework")


@login_required
def delete_course(request, course_id):
    # Ensure the request is POST for security reasons
    if request.method != "POST":
        # If the request is not POST, redirect to a safe page; here, we use the course detail page
        messages.error(
            request, "Invalid request method."
        )  # Optional: Inform the user about the error
        return redirect(
            "course_detail", course_id=course_id
        )  # Adjust the redirect as needed

    course = get_object_or_404(Course, id=course_id)

    if course.instructor != request.user:
        # Redirect or show an error if the user is not authorized to delete this course
        messages.error(
            request, "You are not authorized to delete this course."
        )  # Optional: Inform the user about the error
        return redirect(
            "course_detail", course_id=course_id
        )  # Adjust the redirect as needed

    # Delete the course
    course.delete()

    # Optional: Provide a success message upon deletion
    messages.success(request, "Course deleted successfully.")

    # Redirect to the course list page or another appropriate page
    return redirect("coursework")





@login_required
def course_detail_view(request, course_id):
    # Fetch the course using the course_id
    course = get_object_or_404(Course, id=course_id)

    # Determine if the course has started
    has_started = course.start_date <= now().date()

    # Filter assignments specifically for this course
    assignments = course.assignments.prefetch_related('submissions').all()

    # Apply search query to the filtered assignments if present
    search_query = request.GET.get('search_query', '')
    if search_query:
        assignments = assignments.filter(name__icontains=search_query)

    user_courses = UserCourse.objects.filter(course=course).select_related('user')
    user_ids = [user_course.user.id for user_course in user_courses]
    students = UserProfile.objects.filter(user__id__in=user_ids, role=UserProfile.STUDENT)

    student_average_grades = {}
    for student in students:
        average_grade = Submission.objects.filter(
            student_id=student.user.id,
            assignment__course_id=course_id
        ).aggregate(Avg('grade'))['grade__avg']
        
        student_average_grades[student.user.id] = average_grade if average_grade is not None else 'No grade'

    user_profile = get_object_or_404(UserProfile, user=request.user)
    is_instructor = user_profile.role == UserProfile.INSTRUCTOR

    assignments_submission_status = {}
    for assignment in assignments:
        not_available = assignment.start_date > now().date()
        submissions = assignment.submissions.filter(student=request.user)
        submission_exists = submissions.exists()
        is_late = False
        submission_count = 0
        student_grade = None

        if submission_exists:
            latest_submission = submissions.latest('submitted_at')
            is_late = assignment.end_date < latest_submission.submitted_at.date() if assignment.end_date else False
            student_grade = latest_submission.grade
        
        if is_instructor:
            submission_count = assignment.submissions.count()

        assignments_submission_status[assignment.id] = {
            'submitted': submission_exists,
            'is_late': is_late,
            'submission_count': submission_count,
            'grade': student_grade,
            'assignment_name': assignment.name,
            'assignment_id': assignment.id,
            'not_available': not_available,  # Add this status to the dictionary
        }

    if request.method == 'POST':
        form = AssignmentForm(request.POST, course_id=course_id)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.course = course
            assignment.save()

            formset = AttachmentFormSet(request.POST, request.FILES, instance=assignment)
            if formset.is_valid():
                formset.save()
                return redirect(f'{reverse("view_course", args=[course.id])}?tab=assignments')
    else:
        form = AssignmentForm(course_id=course_id)
        formset = AttachmentFormSet(instance=Assignment())

    context = {
        'form': form,
        'formset': formset,
        'course': course,
        'assignments': assignments,
        'is_instructor': is_instructor,
        'assignments_submission_status': assignments_submission_status,
        'students': students,
        'student_average_grades': student_average_grades,
        'has_started': has_started,
    }

    return render(request, 'coursework/view_course.html', context)


@login_required
def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    # Check if the request.user is the instructor of the course or has other permissions
    if course.instructor != request.user:
        messages.error(request, "You are not authorized to edit this course.")
        return redirect('course_detail', course_id=course_id)

    if request.method == "POST":
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, "Course updated successfully.")
            return redirect('view_course', course_id=course_id)
    else:
        form = CourseForm(instance=course)

    return render(request, 'coursework/edit_course.html', {'form': form, 'course': course})





@login_required
def create_course(request):
    if request.method == "POST":
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            # Temporarily save the course to assign an instructor before committing to the database
            course = form.save(commit=False)
            course.instructor = request.user  # Set the current user as the instructor
            course.save()  # Commit the course to the database

            # Automatically enroll the user in the course they just created
            # Here, we assume the user should be added as an instructor.
            # If you have different roles, adjust accordingly.
            UserCourse.objects.create(user=request.user, course=course)
            
            # Redirect to a success page or the list of courses
            messages.success(request, "Course created and you were enrolled successfully.")
            return redirect("coursework")
    else:
        form = CourseForm()
    return render(request, "coursework/create_course.html", {"form": form})

@login_required
def add_user_to_course(request):
    if request.method == "POST":
        form = UserCourseForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data["user"]
            course = form.cleaned_data["course"]

            # Check if the user is already associated with the course
            if UserCourse.objects.filter(user=user, course=course).exists():
                # User is already in the course, so display an error message
                return redirect("coursework")  # fix later!@
            else:
                # Create the association since it doesn't exist
                UserCourse.objects.create(user=user, course=course)
                # Redirect to a new URL: adjust as needed
                return redirect("coursework")
    else:
        form = UserCourseForm()
    return render(request, "coursework/add_user_to_course.html", {"form": form})

from django.shortcuts import render, get_object_or_404
from django.utils.timezone import now

@login_required
def coursework_view(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    
    # Fetch all courses related to the user and order them by the 'order' field
    user_courses_query = UserCourse.objects.filter(user=request.user).select_related("course").order_by('order')
    
    # Filter active courses: those whose start_date is in the past (or today) and end_date is in the future
    today = now().date()
    active_courses = user_courses_query.filter(course__start_date__lte=today, course__end_date__gt=today)
    
    # Filter past courses: those whose end_date is in the past
    past_courses = user_courses_query.filter(course__end_date__lt=today)
    
    # Filter future courses
    future_courses = user_courses_query.filter(course__start_date__gt=today)

    is_instructor = user_profile.role == UserProfile.INSTRUCTOR
    
    return render(
        request,
        "coursework/view_courses.html",
        {
            "user_courses": active_courses,  # Now correctly includes courses between start and end dates
            "past_courses": past_courses,
            "page_title": "Coursework - Tally",
            "is_instructor": is_instructor,
            'future_courses': future_courses,
        },
    )


@login_required
def download_attachment(request, attachment_id):
    attachment = get_object_or_404(Attachment, id=attachment_id)
    try:
        return FileResponse(
            attachment.file.open(), as_attachment=True, filename=attachment.file.name
        )
    except FileNotFoundError:
        raise Http404("File does not exist")


@login_required
def direct_enroll(request, user_id):
    user = get_object_or_404(UserProfile, id=user_id)
    
    if request.method == "POST":
        form = UserCourseForm(request.POST, user=user)
        if form.is_valid():
            form.save()
            messages.success(request, "User enrolled in the course successfully.")
            return redirect('coursework')  # Adjust the redirect as needed
    else:
        form = UserCourseForm(user=user)
    
    return render(request, "coursework/direct_enroll.html", {'form': form, 'user_id': user_id})


@login_required
def enrolled_members(request, course_id):
    # Fetch the course using the course_id
    course = get_object_or_404(Course, id=course_id)
    
    # Get all UserCourse instances related to the course
    user_courses = UserCourse.objects.filter(course=course)
    
    # Fetch all UserProfile instances from user_courses
    users = [user_course.user for user_course in user_courses]
    
    # Pass the users to the template
    return render(request, "coursework/enrolled_members.html", {"course": course, "users": users})

@login_required
def gradebook(request, course_id):
    # Fetch the course using the course_id
    course = get_object_or_404(Course, id=course_id)

    # Get all UserCourse instances related to the course
    user_courses = UserCourse.objects.filter(course=course).select_related('user')
    
    # Extract the user IDs
    user_ids = [user_course.user.id for user_course in user_courses]
    
    # Fetch all UserProfile instances
    students = UserProfile.objects.filter(user__id__in=user_ids, role=UserProfile.STUDENT)

    # Calculate average grades and attach directly to each student object
    for student in students:
        average_grade = Submission.objects.filter(
            student_id=student.user.id,
            assignment__course_id=course_id
        ).aggregate(Avg('grade'))['grade__avg']
        
        # Attach the average grade directly to the student object
        student.average_grade = average_grade if average_grade is not None else 'No grade'

    user_profile = get_object_or_404(UserProfile, user=request.user)
    is_instructor = user_profile.role == UserProfile.INSTRUCTOR

    return render(request, "coursework/gradebook.html", {
        "course": course,
        "students": students,
        "course_id": course_id,
        "is_instructor": is_instructor
    })

from django.db.models import Q
from django.contrib.auth.models import User

from django.db.models import Avg

from django.db.models import Avg

@login_required
def ajax_search_users(request, course_id):
    query = request.GET.get('q', '')

    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return JsonResponse({"error": "Course not found"}, status=404)

    instructor_user_id = course.instructor.id

    students = User.objects.filter(
        usercourse__course=course
    ).exclude(id=instructor_user_id)

    if query:
        students = students.filter(
            Q(username__icontains=query) | Q(email__icontains=query)
        )

    students_data = []
    for student in students:
        # Adjust the filter to span relationships: Submission -> Assignment -> Course
        average_grade = Submission.objects.filter(
            student=student, 
            assignment__course=course  # Adjusted to use 'assignment__course'
        ).aggregate(avg_grade=Avg('grade'))['avg_grade']

        average_grade_str = f"{average_grade:.2f}" if average_grade is not None else "No grade"

        students_data.append({
            "username": student.username,
            "email": student.email,
            "average_grade": average_grade_str,
            "student_id": student.id, 
        })

    return JsonResponse(students_data, safe=False)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import Course
from django.contrib.auth.decorators import login_required

@csrf_exempt
@login_required
@require_POST
def update_course_order(request):
    try:
        course_order = request.POST.getlist('courseOrder[]')
        for index, course_id in enumerate(course_order):
            user_course = UserCourse.objects.get(user=request.user, course_id=course_id)
            user_course.order = index
            user_course.save()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})