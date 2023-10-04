from .models import Resource, ShipSystem, SubSystem, Component, InstalledComponent, InstalledStorageUnit, StoredResource
import logging
import json
from .game_logging import log, init_logs, clear_logs  # Import the new game_logging 

current_tick = 0  # This should be updated as the game progresses

ship = {
    'name': "FSS Adequate",
    'resources': {}
}

# Initialize logging
init_logs()

def advance_game_tick():
    global current_tick
    current_tick += 1
    # Any game logic that advances the state of the game by one tick
    calculate_ship_resources()
    process_ship_systems()

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

    # Handle production
    for resource_name, amount in produces.items():
        # Increase the resource in the ship's available resources
        ship['resources'][resource_name]['available'] += amount
        produce_text += f"{amount} {resource_name}, "

        # Update the database
        stored_resource, created = StoredResource.objects.get_or_create(resource__name=resource_name)
        stored_resource.currently_stored += amount
        stored_resource.save()

    consume_text = consume_text[:-2] if consume_text else "-"
    produce_text = produce_text[:-2] if produce_text else "-"

    log(f"{component.name} in {installed_component.parent_subsystem}/{installed_component.parent_subsystem.parent_system} # In: {consume_text} # Out: {produce_text}")

def get_game_state():
    # Your logic to collect and return the current state of the game
    calculate_ship_resources()

    # Add any additional game state information you may have
    game_state = {
        'resources': ship['resources']
    }

    return game_state

def restart_game():
    global current_tick
    current_tick = 0

    clear_logs()
    calculate_ship_resources()

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
