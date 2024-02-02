from django.contrib import admin
from .models import Course, UserCourse

admin.site.register(Course)
admin.site.register(UserCourse)
