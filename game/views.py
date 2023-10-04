from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.serializers import serialize

from .models import Resource, ShipSystem, SubSystem, Component, InstalledComponent, StorageType
from . import ctrl  # Import the game_controller module
from .game_logging  import parse_logs # Import the new game_logging file


# Create your views here.
def index(request):
    resources = Resource.objects.all()
    systems = ShipSystem.objects.all()
    components = Component.objects.all()
    storage_types = StorageType.objects.all()
    return render(request, 'game/index.html', {
        'resources': resources, 
        'systems': systems, 
        'components': components,
        'storage_types': storage_types
        })


def advance_game_tick_and_get_game_state(request):
    ctrl.advance_game_tick()  # Advance the game by one tick
    game_state = ctrl.get_game_state()  # Get the current game state
    
    return JsonResponse(game_state)

def restart_game(request):
    ctrl.restart_game()
    return HttpResponseRedirect(reverse('main'))

def debug_page(request):
    return render(request,'game/debug.html')

def get_logs(request):
    log_data = parse_logs()
    return JsonResponse({'data': log_data})

def get_data(request):
    systems = serialize('json', ShipSystem.objects.all())
    subsystems = serialize('json', SubSystem.objects.all())
    components = serialize('json', Component.objects.all())
    installed_components = serialize('json', InstalledComponent.objects.all())
    resources = serialize('json',Resource.objects.all())
    return JsonResponse({
        'systems': systems,
        'subsystems': subsystems,
        'components': components,
        'installed_components': installed_components,
        'resources': resources
    }, safe=False)
