from django.urls import path
from . import views, debug_views  # Make sure your views are being imported

urlpatterns = [
    path('', views.index, name='main'),
    path('advance_tick/', views.advance_tick, name='advance_tick'),
    path('restart/', views.restart_game, name='restart_game'),
    path('debug/', debug_views.debug_page, name='debug_page'),
    path('logs/', debug_views.get_logs, name='logs'),
    path('export_data/', debug_views.export_data, name='export_data'),
    path('import_data/', debug_views.import_data, name='import_data'),
    # Add other URL patterns here
]
