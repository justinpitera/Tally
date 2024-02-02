from django.shortcuts import render
from django.views.generic.edit import CreateView
from .models import Message
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from .models import Message
from django.contrib.auth.mixins import LoginRequiredMixin


class SendMessageView(CreateView):
    model = Message
    fields = ['recipient', 'content']
    success_url = '/'  # Adjust this to your inbox URL

    def form_valid(self, form):
        form.instance.sender = self.request.user
        return super().form_valid(form)


class InboxView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'messenger/messenger.html'  # Make sure this points to the correct template
    context_object_name = 'messages'  # This is how the message list will be referred to in your template

    def get_queryset(self):
        # Filters messages where the recipient is the current user and orders them by timestamp
        return Message.objects.filter(recipient=self.request.user).order_by('-timestamp')



def MessengerView(request):
    return render(request, 'messenger/messenger.html', {'page_title': 'Messenger - Tally'})

def ViewMessage(request):
    # Assuming the user is authenticated
    new_messages_count = Message.objects.filter(recipient=request.user, is_read=False).count()

    # Add the count to your context
    context = {
        'new_messages_count': new_messages_count,
        # include other context variables here
    }

    return render(request, 'my_template.html', context)
