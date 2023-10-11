from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.core.serializers import serialize
import json

from .models import Resource, ShipSystem, SubSystem, Component, InstalledComponent, StorageType, StorageUnit, InstalledStorageUnit, StoredResource, World
from . import ctrl  # Import the game_controller module

# Global variables for resource thresholds
AIR_THRESHOLDS = {'Green': 99, 'Yellow': 51, 'Red': 0}
WATER_THRESHOLDS = {'Green': 81, 'Yellow': 51, 'Red': 0}
FOOD_THRESHOLDS = {'Green': 81, 'Yellow': 51, 'Red': 0}
ENERGY_THRESHOLDS = {'Green': 81, 'Yellow': 51, 'Red': 0}


# Create your views here.
def index(request):
    resources = Resource.objects.all()
    systems = ShipSystem.objects.all()
    components = Component.objects.all()
    storage_types = StorageType.objects.all()
    storage_units = StorageUnit.objects.all()
    installed_storage_units = InstalledStorageUnit.objects.all()
    stored_resources = StoredResource.objects.all()
    game_state = ctrl.get_game_state()
    current_tick = World.objects.get(pk=1).current_tick

    print(game_state)

    return render(request, 'game/index.html', {
        'resources': resources,
        'systems': systems,
        'components': components,
        'storage_types': storage_types,
        'storage_units': storage_units,
        'installed_storage_units': installed_storage_units,
        'stored_resources': stored_resources,
        'ship_resources': game_state['resources'],
        'history': json.dumps(game_state['history']),
        'alerts': get_alerts(game_state['resources']),
        'game_time': calculate_gametime(current_tick),
    })


def advance_game_tick_and_get_game_state(request):
    ctrl.advance_game_tick()  # Advance the game by one tick
    game_state = ctrl.get_game_state()  # Get the current game state

    # Prepare the alerts data
    game_state['alerts'] = get_alerts(game_state['resources'])

    # Calculate game time
    game_state['game_time'] = calculate_gametime(game_state['current_tick'])

    # Transform history data to have game time instead of ticks
    transformed_history = []
    for entry in game_state['history']:
        transformed_entry = entry.copy()
        transformed_entry['game_time'] = calculate_short_gametime(entry['tick'])
        del transformed_entry['tick']
        transformed_history.append(transformed_entry)

    game_state['history'] = transformed_history

    return JsonResponse(game_state)

def restart_game(request):
    ctrl.restart_game()
    return HttpResponseRedirect(reverse('main'))

def get_alerts(ship_resources):
    alerts = {}
    thresholds = {
        'Air': AIR_THRESHOLDS,
        'Water': WATER_THRESHOLDS,
        'Food': FOOD_THRESHOLDS,
        'Energy': ENERGY_THRESHOLDS,
    }

    for resource_name, threshold in thresholds.items():
        available = ship_resources[resource_name]['available']
        capacity = ship_resources[resource_name]['capacity']
        percentage = 0 if capacity==0 else (available / capacity) * 100

        if percentage >= threshold['Green']:
            level = 'bg-success'
        elif percentage >= threshold['Yellow']:
            level = 'bg-warning'
        else:
            level = 'bg-danger'

        alerts[resource_name] = {'percentage': round(percentage, 2), 'level': level}

    return alerts

def calculate_gametime(current_tick):
    elapsed_minutes = current_tick * 5

    days = elapsed_minutes // (24 * 60)
    hours = (elapsed_minutes % (24 * 60)) // 60
    minutes = elapsed_minutes % 60

    return f"{days} days, {hours} hours, {minutes} minutes"

def calculate_short_gametime(tick_count):
    total_minutes = tick_count * 5  # 5 minutes per tick

    days = total_minutes // (24 * 60)
    hours = (total_minutes % (24 * 60)) // 60
    minutes = total_minutes % 60

    short_time = ''
    if days > 0:
        short_time += f"{days}:"
    short_time += f"{hours}:{str(minutes).zfill(2)}"

    return short_time
