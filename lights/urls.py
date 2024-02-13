from django.urls import path
from . import views

urlpatterns = [
    path('control_panel/', views.control_panel, name='control_panel'),
    path('add_light/', views.add_light, name='add_light'),
    path('turn_on_all_lights/', views.turn_on_all_lights, name='turn_on_all_lights'),
    path('turn_off_all_lights/', views.turn_off_all_lights, name='turn_off_all_lights'),
    path('set_color/', views.set_color, name='set_color'),
    path('set_all_white/',views.set_all_white, name='set_all_white'),
    path('set_white/<int:bulb_id>',views.set_white, name='set_white'),
    path('set-light-color/<int:light_id>/', views.set_light_color, name='set_light_color'),
]
