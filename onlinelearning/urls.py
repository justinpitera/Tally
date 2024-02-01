from django.urls import path
from .views import onlinelearning_view

urlpatterns = [
    path('online-learning/', onlinelearning_view, name='online-learning'),
]