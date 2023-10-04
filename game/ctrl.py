from .models import Resource, ShipSystem, SubSystem, Component, InstalledComponent
import logging
import json
from .game_logging import log, init_logs, clear_logs  # Import the new game_logging 

current_tick = 0  # This should be updated as the game progresses

# Initialize logging
init_logs()

def advance_game_tick():
    global current_tick
    current_tick += 1
    # Any game logic that advances the state of the game by one tick
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
    sub_system = installed_component.parent_subsystem
    ship_system = sub_system.parent_system
    consumes = component.consumes
    produces = component.produces

    consume_text = ""
    produce_text = ""

    # Handle consumption
    for resource_name, amount in consumes.items():
        resource = Resource.objects.get(name=resource_name)
        resource.quantity -= amount  # Now consumes for just one instance
        resource.save()
        consume_text += f"{amount} {resource_name}, "

    # Handle production
    for resource_name, amount in produces.items():
        resource = Resource.objects.get(name=resource_name)
        resource.quantity += amount  # Now produces for just one instance
        resource.save()
        produce_text += f"{amount} {resource_name}, "

    consume_text = consume_text[:-2] if consume_text else "-"
    produce_text = produce_text[:-2] if produce_text else "-"

    log(f"{component.name} in {installed_component.parent_subsystem}/{installed_component.parent_subsystem.parent_system} # In: {consume_text} # Out: {produce_text}")

def get_game_state():
    # Your logic to collect and return the current state of the game
    resources = Resource.objects.all()
    resource_data = {resource.name: resource.quantity for resource in resources}
    
    # Add any additional game state information you may have
    game_state = {
        'resources': resource_data
    }

    return game_state

def restart_game():
    global current_tick
    current_tick = 0

    clear_logs()

    Resource.objects.all().delete()
    
    # Define starting quantities in a dictionary
    starting_quantities = {
        'Food': 300,
        'Water': 500,
        'Oxygen': 700,
        'Energy': 1000,
        'Hydrogen': 0,
        'FuelCells': 100,
        'WasteWater': 50,
        'Nutrients': 1000,
        'Air': 100
        # Add more resources here as needed
    }
    
    # Create Resource objects based on the dictionary
    for resource_name, quantity in starting_quantities.items():
        Resource.objects.create(name=resource_name, quantity=quantity)
