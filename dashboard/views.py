from datetime import timezone
import random
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Avg
from accounts.models import UserProfile
from assignment.models import Assignment, Submission
from coursework.models import UserCourse
from .models import GradeNotification  
from django.contrib.auth.decorators import login_required 
from django.http import HttpResponseRedirect
from django.utils import timezone
from .messages import MESSAGE_TEMPLATES 
from django.db.models import Avg, F



def get_random_message(assignment_name):
    template = random.choice(MESSAGE_TEMPLATES)
    return template.format(assignment_name=assignment_name)

@login_required
def mark_notification_as_read(request, notification_id):
    # Retrieve the notification and update its 'read' status
    notification = GradeNotification.objects.get(id=notification_id, receiver=request.user)
    notification.read = True
    notification.save()

    # Redirect back to the dashboard or the page from which the request was made
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('dashboard')))

@login_required
def view_feedback(request, notification_id):
    # Retrieve the notification and update its 'read' status
    notification = GradeNotification.objects.get(id=notification_id, receiver=request.user)
    assignment_id = notification.assignment_id
    url_path = reverse('view_assignment', args=(assignment_id,))
    query_string = "?tab=section3"
    url = f"{url_path}{query_string}"
    # Redirect back to the dashboard or the page from which the request was made
    return HttpResponseRedirect(url)



@login_required
def dashboard_view(request):
    grade_notifications = GradeNotification.objects.filter(receiver=request.user, read=False)
    user_profile = UserProfile.objects.get(user=request.user)
    is_instructor = user_profile.role == UserProfile.INSTRUCTOR
    for notification in grade_notifications:
        notification.random_message = get_random_message(notification.assignment.name)

    today = timezone.now().date()
    one_week_away = today + timezone.timedelta(days=7)

    # Filter courses that the current user is enrolled in
    user_courses = UserCourse.objects.filter(user=request.user).values_list('course', flat=True)

    # Identify assignments for which the user already has a submission
    user_submissions = Submission.objects.filter(student_id=request.user).values_list('assignment_id', flat=True)

    available_assignments = Assignment.objects.filter(
        course__in=user_courses,
        start_date__lte=timezone.now(),  # Ensure the start date is on or before today
        end_date__gte=today,  # Ensure the end date is today or in the future
        end_date__lte=one_week_away  # Ensure the end date is within the next week
    ).exclude(
        id__in=user_submissions
    )

        
    submitted_available_assignments = Assignment.objects.filter(
        course__in=user_courses,
        start_date__lte=timezone.now(),  # Ensure the start date is on or before today
        end_date__gte=today,  # Ensure the end date is today or in the future
        end_date__lte=one_week_away,  # Ensure the end date is within the next week
        id__in=user_submissions
    )

        
    # Filter for upcoming assignments within a week
    upcoming_assignments = Assignment.objects.filter(
        course__in=user_courses,
        start_date__gt=today,
        start_date__lte=one_week_away
    )

    print(available_assignments.count())
    print(submitted_available_assignments.count())


   
    overall_average_grade = None
    if not is_instructor:
        overall_average_grade = Submission.objects.filter(student_id=request.user).aggregate(Avg('grade'))['grade__avg']





    average_grades_per_course = None
    # Calculate average grade per course across all students
    average_grades_per_course = Submission.objects.filter(
        assignment__course__in=user_courses
    ).exclude(
        grade__isnull=True  # Exclude submissions where the grade is null
    ).values(
        'assignment__course'  # Group by course
    ).annotate(
        average_grade=Avg('grade')  # Calculate the average grade for the course
    ).annotate(
        course_id=F('assignment__course'),  # Fetch the course ID for later use
        course_name=F('assignment__course__title')  # Fetch the course name for later use
    ).order_by('assignment__course')


    student_average_grades_per_course = None
    if not is_instructor:
        # Calculate average grade per course for the student
        student_average_grades_per_course = Submission.objects.filter(
            student_id=request.user, 
            assignment__course__in=user_courses
        ).exclude(
            grade__isnull=True  # Exclude submissions where the grade is null
        ).values(
            'assignment__course'  # Group by course
        ).annotate(
            average_grade=Avg('grade')
        ).annotate(
            course_id=F('assignment__course'),  # Fetch the course ID for later use
            course_name=F('assignment__course__title')  
        ).order_by('assignment__course')

    available_assignments_count = available_assignments.count() + submitted_available_assignments.count()
    is_instructor = user_profile.role == UserProfile.INSTRUCTOR

    context = {
        'page_title': 'Dashboard - Tally',
        'grade_notifications': grade_notifications,
        'student_average_grades_per_course': student_average_grades_per_course,  
        'average_grades_per_course': average_grades_per_course,
        'available_assignments': available_assignments,
        'submitted_available_assignments': submitted_available_assignments,  
        'upcoming_assignments': upcoming_assignments,
        'overall_average_grade': overall_average_grade,
        'available_assignments_count':available_assignments_count,
        'is_instructor': is_instructor,
    }

    return render(request, 'dashboard/dashboard.html', context)
