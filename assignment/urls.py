from django.urls import path, include
from .views import create_assignment
from . import views

urlpatterns = [
    # Other URL patterns
    path('create', views.create_assignment, name='create_assignment'),
    path('assignment-list', views.AssignmentListView.as_view(), name='assignment-list'),
]