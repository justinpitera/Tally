from django.urls import path
from .views import coursework_view
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('coursework/', coursework_view, name='coursework'),
    path('coursework/add_user_to_course/', views.add_user_to_course, name='add_user_to_course'),
    path('coursework/create_course/', views.create_course, name='create_course'),
    path('coursework/<int:course_id>/', views.view_course, name='view_course'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)