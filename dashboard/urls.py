from django.urls import path
from .views import dashboard_view
from . import views

urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    path('notifications/mark-as-read/<int:notification_id>/', views.mark_notification_as_read, name='mark_notification_read'),

]