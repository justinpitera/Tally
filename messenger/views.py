from django.shortcuts import get_object_or_404, render
from django.views.generic.edit import CreateView

from messenger.forms import MessageForm
from .models import Message
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from .models import Message
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

class SendMessageView(CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'messenger/send_message.html'
    success_url = reverse_lazy('inbox')

    def get_form_kwargs(self):
        kwargs = super(SendMessageView, self).get_form_kwargs()
        kwargs['user'] = self.request.user  # Add the current user to form kwargs
        return kwargs

    def form_valid(self, form):
        form.instance.sender = self.request.user
        return super().form_valid(form)

class SendDirectMessageView(CreateView):
    model = Message
    fields = ['content']  # We'll set recipient automatically, so it's not a field the user fills
    success_url = reverse_lazy('inbox')  # Adjust this to your inbox URL
    template_name = 'messenger/direct_message.html'


    def get_initial(self):
        initial = super().get_initial()
        # Get recipient_id from the URL
        recipient_id = self.kwargs.get('recipient_id')
        # Fetch the recipient user object based on the recipient_id
        recipient = get_object_or_404(User, pk=recipient_id)
        # Pre-populate the recipient field with the recipient
        initial['recipient'] = recipient
        return initial

    def form_valid(self, form):
        form.instance.sender = self.request.user
        # Since recipient is now a hidden field, we need to ensure it's not manipulated
        recipient_id = self.kwargs.get('recipient_id')
        form.instance.recipient = get_object_or_404(User, pk=recipient_id)
        return super().form_valid(form)
    
class InboxView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'messenger/inbox.html'  
    context_object_name = 'messages'  

    def get_queryset(self):
        # Filters messages where the recipient is the current user and orders them by timestamp
        return Message.objects.filter(recipient=self.request.user).order_by('-timestamp')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add additional context here
        context['page_title'] = 'Messenger - Tally'
        return context


