from django.shortcuts import render, HttpResponse
from django.http import JsonResponse

from .models import Resource
from . import ctrl  # Import the game_controller module


# Create your views here.
def index(request):
    resources = Resource.objects.all()
    return render(request, 'game/index.html', {'resources': resources})


def advance_game_tick_and_get_game_state(request):
    ctrl.advance_game_tick()  # Advance the game by one tick
    game_state = ctrl.get_game_state()  # Get the current game state
    
    return JsonResponse(game_state)
