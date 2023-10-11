from django.db.models import F
import random
from .models import Resource, ShipSystem, SubSystem, Component, InstalledComponent, InstalledStorageUnit, StoredResource, ResourceHistory, World
from .game_logging import log, init_logs, clear_logs  # Import the new game_logging 

ship_name = "FSS Adequate"

aggregated = None

# Initialize logging
init_logs()

def advance_game_tick():
    # advance tick
    world = World.objects.get(pk=1)  # Assuming you have only one game state
    world.current_tick += 1
    world.save()

    # Reset aggregation variables for the new tick
    global aggregated
    aggregated.reset()
            
    # Any game logic that advances the state of the game by one tick
    process_ship_systems()
    
    # Update resource history and aggregated data
    updateResourceHistory()
 
def process_ship_systems():
    # Create an empty list to hold all installed components
    all_installed_components = []

    ship_systems = ShipSystem.objects.all()

    for system in ship_systems:
        # Process each subsystem for this ship system
        subsystems = SubSystem.objects.filter(parent_system=system)

        for subsystem in subsystems:
            installed_components = InstalledComponent.objects.filter(parent_subsystem=subsystem)
            all_installed_components.extend(installed_components)

    # Shuffle the list of all installed components
    random.shuffle(all_installed_components)

    # Process each installed component
    for component in all_installed_components:
        process_installed_component(component)

def process_installed_component(installed_component):
    component = installed_component.component

    # Capture start state for the logs
    ic = installed_component
    msg_start = f"START:%s - %s, IN: %s, OUT: %s" % (ic.component.name, ic.state, ic.input_buffer, ic.output_buffer)

    # Step 1: INTAKE: Take-in required resources
    if installed_component.state == 'INTAKE':
        all_resources_available = True  # Initialize a flag to check if all resources are available
        for resource_name, amount in component.consumes.items():
            # Take available resources into input buffer, up to required amount
            available = aggregated.available_amount[resource_name]
            resources_consumed = min(amount, available)
            installed_component.input_buffer[resource_name] = resources_consumed

            # Update stored resource in db
            store_resources(resource_name, resources_consumed)

            # Update aggregated data
            aggregated.consumed_in_tick[resource_name] += resources_consumed
            aggregated.update()

            # Check if all resources required for production cycle are available
            if resources_consumed < amount:
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
            installed_component.output_buffer = component.produces.copy()
        installed_component.save()

    # Step 3: OUTPUT: Produce resources and send them to storage
    elif installed_component.state == 'OUTPUT':
        # Substep 3.1: Output produced resources
        output_buffer_cleared = True  # Initialize a flag to check if the output buffer is cleared

        for resource_name, amount in installed_component.output_buffer.items():
            available_capacity = aggregated.total_capacity[resource_name] - aggregated.available_amount[resource_name]
            actual_output = min(amount, available_capacity)

            # Update StoredResource and logs
            store_resources(resource_name, actual_output)

            # Update the output buffer
            installed_component.output_buffer[resource_name] -= actual_output

            # Update aggregated data
            aggregated.produced_in_tick[resource_name] += actual_output
            aggregated.update()

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

def get_game_state():
    # Collect current resources data
    resources_data = {}
    for resource in Resource.objects.all():
        if resource.name not in resources_data:
            resources_data[resource.name] = {}
        resources_data[resource.name]['available'] = aggregated.available_amount[resource.name]
        resources_data[resource.name]['capacity'] = aggregated.total_capacity[resource.name]

    # Fetch the resource history data
    history_data = list(ResourceHistory.objects.values('tick', 'quantity_data', 'production_data', 'consumption_data'))

    # Add any additional game state information you may have
    game_state = {
        'resources': resources_data,
        'history': history_data,
        'current_tick': World.objects.get(pk=1).current_tick
    }

    return game_state

def restart_game():
    # Reset World
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

    # Reset AggregatedData and ResourceHistory
    global aggregated
    aggregated = AggregatedData()
    aggregated.reset()
    updateResourceHistory()

class AggregatedData:
    def __init__(self):
        self.produced_in_tick = {}
        self.consumed_in_tick = {}
        self.available_amount = {}
        self.total_capacity = {}
        self.available_capacity = {}

    def reset(self):
        # Reset produced and consumed amounts
        self.produced_in_tick = {}
        self.consumed_in_tick = {}
                
        # Initialize aggregated data for each resource type
        for resource in Resource.objects.all():
            self.produced_in_tick[resource.name] = 0
            self.consumed_in_tick[resource.name] = 0
            self.available_amount[resource.name] = 0
            self.total_capacity[resource.name] = 0
            self.available_capacity[resource.name] = 0

        # Recalculate available amount and capacity
        self.recalculate_amount_and_capacity()

    def update(self):
        self.recalculate_amount_and_capacity()

    def recalculate_amount_and_capacity(self):
        # Iterate through all InstalledStorageUnits
        for installed_unit in InstalledStorageUnit.objects.all():
            # Fetch the corresponding StoredResources
            stored_resources = StoredResource.objects.filter(storage_unit=installed_unit)
            
            # Update the aggregated data
            for stored_resource in stored_resources:
                resource_name = stored_resource.resource.name
                self.available_amount[resource_name] += stored_resource.currently_stored
                self.total_capacity[resource_name] += installed_unit.storage_unit.capacity
                self.available_capacity[resource_name] = self.total_capacity[resource_name] - self.available_amount[resource_name]

def store_resources(resource_name, amount):
    # Query all eligible StoredResource objects
    eligible_stored_resources = StoredResource.objects.filter(
        resource__name=resource_name
    ).annotate(
        remaining_capacity=F('storage_unit__storage_unit__capacity') - F('currently_stored')
    ).order_by('-remaining_capacity')

    remaining_to_store = amount

    # Store the resources
    for stored_resource in eligible_stored_resources:
        space_available = min(stored_resource.remaining_capacity, remaining_to_store)
        stored_resource.currently_stored += space_available
        stored_resource.save()
        remaining_to_store -= space_available

        if remaining_to_store <= 0:
            break

def updateResourceHistory():
    aggregated.update()

    # Store this data in your Django model
    ResourceHistory.objects.create(
        tick=World.objects.get(pk=1).current_tick, 
        quantity_data=aggregated.available_amount,
        production_data=aggregated.produced_in_tick, 
        consumption_data=aggregated.consumed_in_tick
    )
