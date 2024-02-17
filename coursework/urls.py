from django.urls import path
from .views import coursework_view
from . import views
from django.conf import settings
from django.conf.urls.static import static
from assignment.views import AssignmentListView


urlpatterns = [
    path('coursework/', coursework_view, name='coursework'),
    path('coursework/add_user_to_course/', views.add_user_to_course, name='add_user_to_course'),
    path('coursework/delete/<int:course_id>', views.delete_course, name='delete_course'),
    path('course/<int:course_id>/unenroll/<int:user_id>/', views.direct_unenroll, name='direct_unenroll'),
    path('coursework/direct_enroll/<int:user_id>/', views.direct_enroll, name='direct_enroll'),
    path('courses/<int:course_id>/gradebook/', views.gradebook, name='gradebook'),
    path('ajax/search-users/<int:course_id>/', views.ajax_search_users, name='ajax_search_users'),
    path('course/<int:course_id>/edit/', views.edit_course, name='edit_course'),
    path('coursework/create_course/', views.create_course, name='create_course'),
    path('coursework/<int:course_id>/', views.course_detail_view, name='view_course'),
    path('coursework/<int:course_id>/assignments/', AssignmentListView.as_view(), name='course_assignments'),
    path('attachments/download/<int:attachment_id>/', views.download_attachment, name='download_attachment'),
    path('courses/<int:course_id>/members/', views.enrolled_members, name='enrolled_members'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)