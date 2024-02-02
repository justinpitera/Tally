from django.urls import path
from .views import dashboard_view
from . import views

urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    path('hello/', views.hello_user, name='hello_user'),
]