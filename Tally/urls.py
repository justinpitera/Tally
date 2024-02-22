
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Other URL patterns
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls')),
    path('', include('messenger.urls')),
    path('', include('onlinelearning.urls')),
    path('', include('coursework.urls')),
    path('accounts/', include('accounts.urls')),
    path('assignment/', include('assignment.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)