from django.urls import path
from .views import SendMessageView, InboxView
from . import views

urlpatterns = [
    path('messenger/', views.MessengerView, name='messenger'),
    path('send/', SendMessageView.as_view(), name='send_message'),
    path('inbox/', InboxView.as_view(), name='inbox'),
]
