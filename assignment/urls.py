from django.urls import path, include
#from .views import create_assignment
from . import views

urlpatterns = [
    #path('create/<int:course_id>', views.create_assignment, name='create_assignment'),
    path('list/<int:course_id>/', views.AssignmentListView.as_view(), name='assignment_list'),
    path('view/<int:assignment_id>/', views.view_assignment, name='assignment_view'),
    path('attachments/download/<int:attachment_id>/', views.download_attachment, name='download_attachment'),
    path('submit/<int:assignment_id>/', views.submit_assignment, name='submit_assignment'),
    path('is_submitted/<int:student_id>/<int:assignment_id>/', views.is_submitted, name='is_submitted'),
    path('submission/grade/<int:submission_id>/', views.grade_submission, name='grade_submission'),
    path('grades/<int:course_id>', views.CourseGradesView.as_view(), name='course_grades'),
    path('submissions/<int:submission_id>/feedback/add/', views.add_feedback, name='add_feedback'),
    path('<int:assignment_id>/edit/', views.edit_assignment, name='edit_assignment'),
    path('course/<int:course_id>/create_assignment/', views.create_assignment, name='create_assignment'),
]