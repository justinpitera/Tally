from django.shortcuts import render

def dashboard_view(request):
    return render(request, 'dashboard/dashboard.html', {'page_title': 'Dashboard - Tally'})

