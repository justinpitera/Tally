from django.urls import path, include

from dashboard import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
]
