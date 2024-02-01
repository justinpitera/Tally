from django.urls import path
from .views import upcoming_view
urlpatterns = [
    path('upcoming/', upcoming_view, name='upcoming'),
]