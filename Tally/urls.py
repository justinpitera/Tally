
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Other URL patterns
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls')),
    path('', include('messenger.urls')),
    path('', include('onlinelearning.urls')),
    path('', include('coursework.urls')),
    path('', include('upcoming.urls')),
    path('accounts/', include('accounts.urls')),
]
