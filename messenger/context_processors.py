# context_processors.py
from .models import Message

def new_messages_processor(request):
    if request.user.is_authenticated:
        return {'new_messages_count': Message.objects.filter(recipient=request.user, is_read=False).count()}
    else:
        return {'new_messages_count': 0}
