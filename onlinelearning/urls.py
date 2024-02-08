from django.urls import path

from onlinelearning import views
from .views import onlinelearning_view

urlpatterns = [
    path('online-learning/', onlinelearning_view, name='online-learning'),
    path('coursework/<int:course_id>/modules/create/', views.create_module, name='create_module'),
    path('submit/<module_arg>/', views.submit_content, name='submit_content'),
    path('modules/<int:module_id>/', views.module_view, name='module_view'),
    path('content/delete/<int:content_id>/', views.delete_custom_content, name='delete_custom_content'),
]