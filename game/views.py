from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse

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
    return render(request, 'game/index.html', context)

def advance_tick(request):
    ctrl.advance_game_tick()
    context = prepare_context()
    return JsonResponse(context)

def get_data(request):
    context = prepare_context()
    return JsonResponse(context)

def restart_game(request):
    ctrl.restart_game()
    return HttpResponseRedirect(reverse('main'))

def prepare_context():
    # Prepare context
    context = {
        'resources': list(Resource.objects.all().values()),
        'systems': list(ShipSystem.objects.all().values()),
        'subsystems': list(SubSystem.objects.all().values()),
        'components': list(Component.objects.all().values()),
        'storage_types': list(StorageType.objects.all().values()),
        'storage_units': list(StorageUnit.objects.all().values()),
        'installed_storage_units': list(InstalledStorageUnit.objects.all().values()),
        'installed_components': list(InstalledComponent.objects.all().values()),
        'stored_resources': list(StoredResource.objects.all().values()),
        'alerts': get_alerts(),
        'game_time': calculate_gametime(World.objects.get(pk=1).current_tick),
        'resource_data': get_resource_data(),
        'history_data': prepare_history(),
        'ship_systems': prepare_ship_systems()
    }

    return context

def prepare_ship_systems():
    ship_systems = []
    for system in ShipSystem.objects.all():
        system_dict = {'name': system.name, 'subsystems': []}
        for subsystem in system.subsystems.all():
            subsystem_dict = {'name': subsystem.name, 'components': []}
            for installed_component in subsystem.components.all():
                component_dict = {'name': installed_component.component.name}
                subsystem_dict['components'].append(component_dict)
            system_dict['subsystems'].append(subsystem_dict)
        ship_systems.append(system_dict)
    return ship_systems


def prepare_history():
    history = list(ResourceHistory.objects.all().values())
    transformed_history = []
    for entry in history:
        transformed_entry = entry.copy()
        transformed_entry['game_time'] = calculate_short_gametime(entry['tick'])
        del transformed_entry['tick']
        transformed_history.append(transformed_entry)
    return transformed_history

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
