from django.shortcuts import render, HttpResponse
from .models import Resource


# Create your views here.
def index(request):
    resources = Resource.objects.all()
    return render(request, 'game/index.html', {'resources': resources})
