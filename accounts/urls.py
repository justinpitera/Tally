from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/', views.Register, name='register'),
    path('login/', views.UserLogin, name='login'),
    path('logout/', views.UserLogout, name='logout'),
    path('profile/<int:user_id>/', views.view_profile, name='view_profile'),  
]
