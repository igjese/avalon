from .models import Resource, ShipSystem, SubSystem, Component, InstalledComponent, InstalledStorageUnit, StoredResource, ResourceHistory, World
import logging
import json
from .game_logging import log, init_logs, clear_logs  # Import the new game_logging 

ship = {
    'name': "FSS Adequate",
    'resources': {}
}

# aggregated production and consumption data for single tick
aggregated_production = {}
aggregated_consumption = {}


# Initialize logging
init_logs()

def advance_game_tick():
    # advance tick
    world = World.objects.get(pk=1)  # Assuming you have only one game state
    world.current_tick += 1
    world.save()

    # Reset aggregation variables for the new tick
    global aggregated_production
    global aggregated_consumption
        
    for resource_name in ship['resources'].keys():
        aggregated_production[resource_name] = 0
        aggregated_consumption[resource_name] = 0
    
    # Any game logic that advances the state of the game by one tick
    calculate_ship_resources()
    process_ship_systems()
    
    # Update resource history and aggregated data
    updateResourceHistory()

def updateResourceHistory():
    # Capture current resource state
    resource_quantity = {}
    for resource_name, resource_info in ship['resources'].items():
        resource_quantity[resource_name] = resource_info['available']
    
    # Store this data in your Django model
    ResourceHistory.objects.create(
        tick=World.objects.get(pk=1).current_tick, 
        quantity_data=resource_quantity, 
        production_data=aggregated_production, 
        consumption_data=aggregated_consumption
    )
 

def process_ship_systems():
    ship_systems = ShipSystem.objects.all()

    for system in ship_systems:
        # Process each subsystem for this ship system
        subsystems = SubSystem.objects.filter(parent_system=system)

        for subsystem in subsystems:
            process_subsystem(subsystem)

def process_subsystem(sub_system):
    installed_components = InstalledComponent.objects.filter(parent_subsystem=sub_system)
    for installed_component in installed_components:
        for _ in range(installed_component.quantity):
            process_installed_component(installed_component)

def process_installed_component(installed_component):
    component = installed_component.component
    consumes = component.consumes
    produces = component.produces

    # Check if enough resources are available for consumption
    can_consume = all(ship['resources'][resource_name]['available'] >= amount for resource_name, amount in consumes.items())

    # Check if enough capacity is available for production
    can_produce = all(ship['resources'][resource_name]['available'] + amount <= ship['resources'][resource_name]['capacity'] for resource_name, amount in produces.items())

    if can_consume and can_produce:
        consume_text = ""
        produce_text = ""

        # Handle consumption
        for resource_name, amount in consumes.items():
            # Reduce the resource in the ship's available resources
            ship['resources'][resource_name]['available'] -= amount
            consume_text += f"{amount} {resource_name}, "

            # Update the database
            stored_resource = StoredResource.objects.get(resource__name=resource_name)
            stored_resource.currently_stored -= amount
            stored_resource.save()

            # Update aggregated consumption
            for resource_name, amount in consumes.items():
                aggregated_consumption[resource_name] = aggregated_consumption.get(resource_name, 0) + amount

        # Handle production
        for resource_name, amount in produces.items():
            # Increase the resource in the ship's available resources
            ship['resources'][resource_name]['available'] += amount
            produce_text += f"{amount} {resource_name}, "

            # Update the database
            stored_resource, created = StoredResource.objects.get_or_create(resource__name=resource_name)
            stored_resource.currently_stored += amount
            stored_resource.save()

            # Update aggregated production
            for resource_name, amount in produces.items():
                aggregated_production[resource_name] = aggregated_production.get(resource_name, 0) + amount

        consume_text = consume_text[:-2] if consume_text else "-"
        produce_text = produce_text[:-2] if produce_text else "-"

        log(f"{component.name} in {installed_component.parent_subsystem}/{installed_component.parent_subsystem.parent_system} # In: {consume_text} # Out: {produce_text}")
 
    else:
        # Log or handle the case where the component can't process due to insufficient resources or capacity
        log(f"Component {component.name} could not process due to insufficient resources or capacity.")

def get_game_state():
    # Your logic to collect and return the current state of the game
    calculate_ship_resources()

    # Fetch the resource history data
    history_data = list(ResourceHistory.objects.values('tick', 'quantity_data', 'production_data', 'consumption_data'))

    # Add any additional game state information you may have
    game_state = {
        'resources': ship['resources'],
        'history': history_data,
        'current_tick': World.objects.get(pk=1).current_tick
    }

    return game_state

def restart_game():
    world = World.objects.get(pk=1)
    world.current_tick = 0
    world.save()

    # Delete all records from the ResourceHistory table
    ResourceHistory.objects.all().delete()

    # Reset resource quantities to half of their storage capacities
    StoredResource.objects.filter(resource__name='Energy').update(currently_stored=50)
    StoredResource.objects.filter(resource__name='Air').update(currently_stored=100)
    StoredResource.objects.filter(resource__name='Food').update(currently_stored=50)
    StoredResource.objects.filter(resource__name='FuelCells').update(currently_stored=500)
    StoredResource.objects.filter(resource__name='Hydrogen').update(currently_stored=50)
    StoredResource.objects.filter(resource__name='Nutrients').update(currently_stored=500)
    StoredResource.objects.filter(resource__name='Oxygen').update(currently_stored=50)
    StoredResource.objects.filter(resource__name='WasteWater').update(currently_stored=250)
    StoredResource.objects.filter(resource__name='Water').update(currently_stored=250)

    clear_logs()
    calculate_ship_resources()

    # Reset aggregation variables for the new tick
    global aggregated_production
    global aggregated_consumption
        
    for resource_name in ship['resources'].keys():
        aggregated_production[resource_name] = 0
        aggregated_consumption[resource_name] = 0

    updateResourceHistory()
    
def calculate_ship_resources():
    # Reset to zero for each tick
    for resource_key in ship['resources']:
        ship['resources'][resource_key]['available'] = 0
        ship['resources'][resource_key]['capacity'] = 0

    # Get all installed storage units for the ship
    installed_storage_units = InstalledStorageUnit.objects.all()

    # Aggregate available and capacity for each resource from InstalledStorageUnit
    for unit in installed_storage_units:
        # Access StoredResource objects related to this InstalledStorageUnit
        stored_resources = StoredResource.objects.filter(storage_unit=unit)

        for stored_resource in stored_resources:
            resource_name = stored_resource.resource.name
            storage_type = unit.storage_unit.storage_type  # Assuming you can access the storage type like this

            if resource_name not in ship['resources']:
                ship['resources'][resource_name] = {'available': 0, 'capacity': 0, 'storage_type': storage_type}

            ship['resources'][resource_name]['available'] += stored_resource.currently_stored

            # Aggregate capacity for each installed storage unit
            ship['resources'][resource_name]['capacity'] += unit.storage_unit.capacity * unit.quantity
            ship['resources'][resource_name]['storage_type'] = storage_type.name  # Added this line to update the storage type
