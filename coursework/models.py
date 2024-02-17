from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='taught_courses', null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    image = models.ImageField(upload_to='course_images/', null=True, blank=True)
    syllabus = models.FileField(upload_to='submissions/%Y/%m/%d/', null=True)

    def __str__(self):
        return self.title


class UserCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrollment_date = models.DateField(auto_now_add=True)
    order = models.IntegerField(default=0)  # Add this line

    class Meta:
        unique_together = (('user', 'course'),)
        ordering = ['order']
    
    def __str__(self):
        return f"{self.user.username} - {self.course.title}"


class UserCourseOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    order = models.IntegerField(default=0)

    class Meta:
        unique_together = ('user', 'course')
        ordering = ['order']

    def __str__(self):
        return f'{self.user.username} - {self.course.title} - {self.order}'


