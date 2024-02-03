from django.db import models
from django.contrib.auth.models import User
from coursework.models import Course

class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments', null=True)
    name = models.CharField(max_length=200)
    instruction = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        # This should return 'self.name' instead of 'self.title'
        return self.name

class Attachment(models.Model):
    assignment = models.ForeignKey(Assignment, related_name='attachments', on_delete=models.CASCADE)
    file = models.FileField(upload_to='assignment_attachments/')
    
    def __str__(self):
        return f"Attachment for {self.assignment.name}"



