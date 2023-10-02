from django.urls import path
from . import views  # Make sure your views are being imported

urlpatterns = [
    path('', views.index, name='index'),
    path('advance_game_tick_and_get_game_state/', views.advance_game_tick_and_get_game_state, name='advance_game_tick_and_get_game_state'),
    # Add other URL patterns here
]
