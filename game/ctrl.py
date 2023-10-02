from .models import Resource  # Assuming your Resource model is in a file called models.py

def advance_game_tick():
    # Any game logic that advances the state of the game by one tick
    consume_resources()

def consume_resources():
    resources = Resource.objects.all()  # Fetch all resources from the database
    
    for resource in resources:
        if resource.quantity > 0:
            resource.quantity -= 1  # Consume 1 of each resource
            resource.save()  # Save the updated resource back to the database

def get_game_state():
    # Your logic to collect and return the current state of the game
    resources = Resource.objects.all()
    resource_data = {resource.name: resource.quantity for resource in resources}
    
    # Add any additional game state information you may have
    game_state = {
        'resources': resource_data
    }
    
    return game_state
