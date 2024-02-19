from django.db import models
from django.contrib.auth.models import User
from coursework.models import Course
from assignment.models import Assignment

class GradeNotification(models.Model):
    # Course and receiver of the notification
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, null=True)

    # Student
    receiver = models.ForeignKey(User, related_name='receiver_notifications', on_delete=models.CASCADE)
    
    # Grade comments
    comments = models.TextField()
    
    # Timestamp for when the notification was generated (when the assignment was graded)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # Boolean field to track whether the notification has been read
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Grade recieved for {self.receiver} from {self.course} at {self.timestamp}"

    # Method to mark the notification as read
    def mark_as_read(self):
        self.read = True
        self.save()

    class Meta:
        ordering = ['-timestamp']  # Order notifications by most recent
