from .models import Resource, ShipSystem, SubSystem, Component, InstalledComponent
import json

def advance_game_tick():
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
    consumes = component.consumes
    produces = component.produces

    # Handle consumption
    for resource_name, amount in consumes.items():
        resource = Resource.objects.get(name=resource_name)
        resource.quantity -= amount  # Now consumes for just one instance
        resource.save()

    # Handle production
    for resource_name, amount in produces.items():
        resource = Resource.objects.get(name=resource_name)
        resource.quantity += amount  # Now produces for just one instance
        resource.save()

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
    Resource.objects.all().delete()
    Resource.objects.create(name='Food', quantity=300)
    Resource.objects.create(name='Water', quantity=500)
    Resource.objects.create(name='Oxygen', quantity=700)
    Resource.objects.create(name='Energy', quantity=1000)
