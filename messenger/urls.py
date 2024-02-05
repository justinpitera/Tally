from django.urls import path
from .views import SendMessageView, InboxView
from . import views

urlpatterns = [

    path('send/', SendMessageView.as_view(), name='send_message'),
    path('inbox/', InboxView.as_view(), name='inbox'),
]
