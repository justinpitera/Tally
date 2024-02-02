from django.shortcuts import render

def dashboard_view(request):
    return render(request, 'dashboard/dashboard.html', {'page_title': 'Dashboard - Tally'})


def hello_user(request):
    context = {'username': request.user.username}
    return render(request, 'hello_user.html', context)