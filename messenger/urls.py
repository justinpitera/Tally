from django.urls import path
from .views import SendMessageView, InboxView
from . import views

urlpatterns = [

    path('send/', SendMessageView.as_view(), name='send_message'),
    path('send/<recipient_id>/', SendMessageView.as_view(), name='send_message_with_recipient'),
    path('inbox/', InboxView.as_view(), name='inbox'),
]
