from django.shortcuts import render

def coursework_view(request):
    return render(request, 'coursework/coursework.html', {'page_title': 'Coursework - Tally'})