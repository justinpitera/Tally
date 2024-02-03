from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    INSTRUCTOR = 'instructor'
    STUDENT = 'student'
    ROLE_CHOICES = [
        (INSTRUCTOR, 'Instructor'),
        (STUDENT, 'Student'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=STUDENT)
