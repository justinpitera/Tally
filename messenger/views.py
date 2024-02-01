from django.shortcuts import render

def messenger_view(request):
    return render(request, 'messenger/messenger.html', {'page_title': 'Messenger - Tally'})
