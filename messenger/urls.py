from django.urls import path
from .views import messenger_view

urlpatterns = [
    path('messenger/', messenger_view, name='messenger'),
]