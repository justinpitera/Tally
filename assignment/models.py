from django.db import models
from coursework.models import Course
from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone



class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments', null=True)
    name = models.CharField(max_length=200)
    instruction = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_submitted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class AssignmentListView(ListView):
    model = Assignment
    template_name = 'assignment/assignment_list.html'
    context_object_name = 'assignments'

    def get_queryset(self):
        course_id = self.kwargs.get('course_id')
        if course_id is not None:
            course = get_object_or_404(Course, id=course_id)
            return course.assignments.all()
        else:
            return Assignment.objects.none() 


class Attachment(models.Model):
    assignment = models.ForeignKey(Assignment, related_name='attachments', on_delete=models.CASCADE)
    file = models.FileField(upload_to='assignment_attachments/')
    
    def __str__(self):
        return f"Attachment for {self.assignment.name}"


class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True, null=True)
    file = models.FileField(upload_to='submissions/%Y/%m/%d/')
    grade = models.IntegerField(null=True, blank=True)
    comments = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f"Submission for {self.assignment.name} by {self.student.username}"

