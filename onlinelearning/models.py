from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from assignment.models import Assignment
from coursework.models import Course




from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings

# Assuming the Module model is already defined as shown in your prompt
    
class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules', null=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)

class CustomContent(models.Model):
    CONTENT_TYPES = (
        ('file', 'File'),
        ('url', 'URL'),
        ('text', 'Text'),
        ('assignment', 'Assignment'),
        ('module', 'Module'),
        ('urltext', 'URLText')
    )
    content_type = models.CharField(max_length=10, choices=CONTENT_TYPES)
    file = models.FileField(upload_to='uploads/%Y/%m/%d/', blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, blank=True, null=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, blank=True, null=True)
    urltext = models.CharField(blank=True, null=True,max_length=120)

    def __str__(self):
        return self.get_content_type_display()


