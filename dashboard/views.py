from datetime import timezone
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Avg
from accounts.models import UserProfile
from assignment.models import Assignment, Submission
from coursework.models import UserCourse
from .models import GradeNotification  # Adjust the import path according to your project structure
from django.contrib.auth.decorators import login_required  # Import to restrict access to logged-in users
from django.http import HttpResponseRedirect
from django.utils import timezone

@login_required
def mark_notification_as_read(request, notification_id):
    # Retrieve the notification and update its 'read' status
    notification = GradeNotification.objects.get(id=notification_id, receiver=request.user)
    notification.read = True
    notification.save()

    # Redirect back to the dashboard or the page from which the request was made
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('dashboard')))


@login_required
def dashboard_view(request):
    unread_notifications = GradeNotification.objects.filter(receiver=request.user, read=False)

    today = timezone.now().date()
    one_week_away = today + timezone.timedelta(days=7)

    # Filter courses that the current user is enrolled in
    user_courses = UserCourse.objects.filter(user=request.user).values_list('course', flat=True)

    # Now filter assignments based on those courses
    available_assignments = Assignment.objects.filter(
        course__in=user_courses,
        start_date__lte=today,
        end_date__gte=today
    )
    upcoming_assignments = Assignment.objects.filter(
        course__in=user_courses,
        start_date__gt=today,
        start_date__lte=one_week_away
    )
    
    overall_average_grade = None

    user_profile = UserProfile.objects.get(user=request.user)
    is_instructor = user_profile.role == UserProfile.INSTRUCTOR
    if not is_instructor:

        overall_average_grade = Submission.objects.filter(student_id=request.user).aggregate(Avg('grade'))['grade__avg']
        
    context = {
        'page_title': 'Dashboard - Tally',
        'grade_notifications': unread_notifications,
        'overall_average_grade': overall_average_grade,  
        'available_assignments': available_assignments,
        'upcoming_assignments': upcoming_assignments,
    }

    return render(request, 'dashboard/dashboard.html', context)
