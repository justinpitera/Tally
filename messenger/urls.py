from django.urls import path
from .views import SendDirectMessageView, SendMessageView, InboxView
from . import views

urlpatterns = [
    path('inbox/', InboxView.as_view(), name='inbox'),
    path('send-message/', SendMessageView.as_view(), name='send_message'),
    path('send-message/<int:recipient_id>/', SendDirectMessageView.as_view(), name='send_message'),
]
