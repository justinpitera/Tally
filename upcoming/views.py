from django.shortcuts import render

def upcoming_view(request):
    return render(request, 'upcoming/upcoming.html', {'page_title': 'Upcoming - Tally'})
