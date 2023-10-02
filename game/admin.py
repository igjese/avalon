# admin.py
from django.contrib import admin
from .models import Resource

class ResourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity')

admin.site.register(Resource, ResourceAdmin)
