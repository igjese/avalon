from .models import Resource, ShipSystem, SubSystem, Component, InstalledComponent, InstalledStorageUnit, StoredResource, ResourceHistory, World
import logging
import json
from .game_logging import log, init_logs, clear_logs  # Import the new game_logging 

ship_name = "FSS Adequate"

class Aggregated:
    def __init__(self):
        self.production = {}
        self.consumption = {}
        self.available_amount = {}
        self.total_capacity = {}
        self.available_capacity = {}

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
        process_installed_component(installed_component)  # Directly process each installed component

def process_installed_component(installed_component):
    component = installed_component.component

    # Capture start state for the logs
    ic = installed_component
    msg_start = f"START:%s - %s, IN: %s, OUT: %s" % (ic.component.name, ic.state, ic.input_buffer, ic.output_buffer)

    # Step 1: INTAKE: Take-in required resources
    if installed_component.state == 'INTAKE':
        # Substep 1.1: Consume input resources
        all_resources_available = True  # Initialize a flag to check if all resources are available
        for resource_name, amount in component.consumes.items():
            available = ship['resources'][resource_name]['available']
            actual_consumption = min(amount, available)
            installed_component.input_buffer[resource_name] = actual_consumption
            ship['resources'][resource_name]['available'] -= actual_consumption
            aggregated_consumption[resource_name] += amount  # Update based on actual consumption

            # Update StoredResource and logs
            update_stored_resource(resource_name, -actual_consumption)

            # Check if all required resources are available
            if actual_consumption < amount:
                all_resources_available = False

        # Transition to 'WORKING' state only if all resources are available
        if all_resources_available:
            installed_component.state = 'WORKING'
            installed_component.remaining_ticks_for_cycle = component.ticks_per_cycle
            installed_component.input_buffer.clear()
            installed_component.save()
        
    # Step 2: WORKING: Work for some ticks
    elif installed_component.state == 'WORKING':
        # Substep 2.1: Count down the remaining ticks
        installed_component.remaining_ticks_for_cycle -= 1

        # Transition to 'OUTPUT' state
        if installed_component.remaining_ticks_for_cycle == 0:
            installed_component.state = 'OUTPUT'
            installed_component.output_buffer = produces.copy()
        installed_component.save()

    # Step 3: OUTPUT: Produce resources and send them to storage
    elif installed_component.state == 'OUTPUT':
        # Substep 3.1: Output produced resources
        output_buffer_cleared = True  # Initialize a flag to check if the output buffer is cleared

        for resource_name, amount in installed_component.output_buffer.items():
            available_capacity = ship['resources'][resource_name]['capacity'] - ship['resources'][resource_name]['available']
            actual_output = min(amount, available_capacity)
            ship['resources'][resource_name]['available'] += actual_output
            aggregated_production[resource_name] += amount  # Update based on actual production

            # Update StoredResource and logs
            update_stored_resource(resource_name, actual_output)

            # Update the output buffer
            installed_component.output_buffer[resource_name] -= actual_output

            # Check if the output buffer is cleared
            if installed_component.output_buffer[resource_name] > 0:
                output_buffer_cleared = False

        # Transition to 'INTAKE' state only if the output buffer is cleared
        if output_buffer_cleared:
            installed_component.state = 'INTAKE'
            installed_component.output_buffer.clear()
        installed_component.save()
        
    # Update logs
    msg_finish = f"FINISH:%s - %s, IN: %s, OUT: %s" % (ic.component.name, ic.state, ic.input_buffer, ic.output_buffer)
    msg_component = f"{component.name} ({ic.parent_subsystem} / {ic.parent_subsystem.parent_system}) - {ic.state}"
    log(msg_component, msg_start, msg_finish)

# Helper functions to update StoredResource and logs
def update_stored_resource(resource_name, amount):
    stored_resource = StoredResource.objects.get(resource__name=resource_name)
    stored_resource.currently_stored += amount
    stored_resource.save()


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

    # Reset states for installed components
    InstalledComponent.objects.all().update(state='INTAKE', input_buffer={}, output_buffer={})

    # Clear logs
    clear_logs()

    # Calculate intermediate results
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
