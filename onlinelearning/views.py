from django.shortcuts import render

def onlinelearning_view(request):
    return render(request, 'onlinelearning/onlinelearning.html', {'page_title': 'Online Learning - Tally'})
