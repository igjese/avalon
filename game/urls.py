from django.urls import path
from . import views  # Make sure your views are being imported

urlpatterns = [
    path('', views.index, name='main'),
    path('advance_game_tick_and_get_game_state/', views.advance_game_tick_and_get_game_state, name='advance_game_tick_and_get_game_state'),
    path('restart/', views.restart_game, name='restart_game'),
    path('debug/', views.debug_page, name='debug_page'),
    path('logs/', views.get_logs, name='logs'),
    path('export_data/', views.export_data, name='export_data'),
    path('import_storage_type/', views.import_storage_type, name='import_storage_type'),
    # Add other URL patterns here
]
