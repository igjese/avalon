from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.core.serializers import serialize
import json

from .models import Resource, ShipSystem, SubSystem, Component, InstalledComponent, StorageType, StorageUnit, InstalledStorageUnit, StoredResource, World, ResourceHistory
from . import ctrl  # Import the game_controller module

# Global variables for resource thresholds
AIR_THRESHOLDS = {'Green': 99, 'Yellow': 51, 'Red': 0}
WATER_THRESHOLDS = {'Green': 81, 'Yellow': 51, 'Red': 0}
FOOD_THRESHOLDS = {'Green': 81, 'Yellow': 51, 'Red': 0}
ENERGY_THRESHOLDS = {'Green': 81, 'Yellow': 51, 'Red': 0}

# Create your views here.
def index(request):
    context = prepare_context()
    return render(request, 'index.html', context)

def advance_game_tick_and_get_game_state(request):
    ctrl.advance_game_tick()
    context = prepare_context()
    return JsonResponse(context)

def restart_game(request):
    ctrl.restart_game()
    return HttpResponseRedirect(reverse('main'))

def prepare_context():
    # Prepare context
    context = {
        'resources': Resource.objects.all(),
        'systems': ShipSystem.objects.all(),
        'subsystems': SubSystem.objects.all(),
        'components': Component.objects.all(),
        'storage_types': StorageType.objects.all(),
        'storage_units': StorageUnit.objects.all(),
        'installed_storage_units': InstalledStorageUnit.objects.all(),
        'installed_components': InstalledComponent.objects.all(),
        'stored_resources': StoredResource.objects.all(),
        'alerts': get_alerts(),
        'game_time': calculate_gametime(World.objects.get(pk=1).current_tick),
        'resource_data': get_resource_data(),
        'history_data': list(ResourceHistory.objects.values('tick', 'quantity_data', 'production_data', 'consumption_data')),
    }

    return context

def get_resource_data():
    from .ctrl import aggregated
    resource_data = {}

    for resource in Resource.objects.all():
        if resource.name not in resource_data:
            resource_data[resource.name] = {}

        resource_data[resource.name]['available'] = aggregated.available_amount[resource.name]
        resource_data[resource.name]['capacity'] = aggregated.total_capacity[resource.name]

    return resource_data

def get_alerts():
    alerts = {}
    thresholds = {
        'Air': AIR_THRESHOLDS,
        'Water': WATER_THRESHOLDS,
        'Food': FOOD_THRESHOLDS,
        'Energy': ENERGY_THRESHOLDS,
    }
    ship_resources = get_resource_data()

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
