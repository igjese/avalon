from django.contrib import admin
from .models import Resource, ShipSystem, SubSystem, Component, InstalledComponent, StorageType, StorageUnit, InstalledStorageUnit, StoredResource, Location, World, ResourceHistory

# Configurations
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'storage_type', 'info')

class ComponentAdmin(admin.ModelAdmin):
    list_display = ('name', 'consumes', 'produces', 'ticks_per_cycle', 'info')

class StorageTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'info')

class StorageUnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'storage_type', 'capacity', 'info')

# Ship Setup
class ShipSystemAdmin(admin.ModelAdmin):
    list_display = ('name',)

class SubSystemAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent_system')

class InstalledComponentAdmin(admin.ModelAdmin):
    list_display = ('component', 'parent_subsystem', 'state', 'input_buffer', 'output_buffer')

class InstalledStorageUnitAdmin(admin.ModelAdmin):
    list_display = ('storage_unit', 'subsystem', 'assigned_resource') 

# Game Data
class StoredResourceAdmin(admin.ModelAdmin):
    list_display = ('storage_unit', 'resource', 'currently_stored')

class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'location_type')

class WorldAdmin(admin.ModelAdmin):
    list_display = ('id','current_tick')

class ResourceHistoryAdmin(admin.ModelAdmin):
    list_display = ('tick', 'quantity_data', 'production_data', 'consumption_data')

admin.site.register(Resource, ResourceAdmin)
admin.site.register(ShipSystem, ShipSystemAdmin)
admin.site.register(SubSystem, SubSystemAdmin)
admin.site.register(Component, ComponentAdmin)
admin.site.register(InstalledComponent, InstalledComponentAdmin)
admin.site.register(StorageType, StorageTypeAdmin)
admin.site.register(StorageUnit, StorageUnitAdmin)
admin.site.register(InstalledStorageUnit, InstalledStorageUnitAdmin)
admin.site.register(StoredResource, StoredResourceAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(World, WorldAdmin)
admin.site.register(ResourceHistory, ResourceHistoryAdmin)
