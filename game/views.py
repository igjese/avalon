from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Resource, ShipSystem
from . import ctrl  # Import the game_controller module


# Create your views here.
def index(request):
    resources = Resource.objects.all()
    systems = ShipSystem.objects.all()
    return render(request, 'game/index.html', {'resources': resources, 'systems': systems})


def advance_game_tick_and_get_game_state(request):
    ctrl.advance_game_tick()  # Advance the game by one tick
    game_state = ctrl.get_game_state()  # Get the current game state
    
    return JsonResponse(game_state)

def restart_game(request):
    ctrl.restart_game()
    return HttpResponseRedirect(reverse('main'))