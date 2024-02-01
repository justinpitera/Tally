from django.urls import path
from .views import coursework_view

urlpatterns = [
    path('coursework/', coursework_view, name='coursework'),
]