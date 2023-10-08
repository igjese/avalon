from django.contrib import admin
from .models import Resource, ShipSystem, SubSystem, Component, InstalledComponent, StorageType, StorageUnit, InstalledStorageUnit, StoredResource, Location, World

class ResourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'storage_type')

class ShipSystemAdmin(admin.ModelAdmin):
    list_display = ('name',)

class SubSystemAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent_system')

class ComponentAdmin(admin.ModelAdmin):
    list_display = ('name', 'consumes', 'produces', 'info')

class InstalledComponentAdmin(admin.ModelAdmin):
    list_display = ('component', 'parent_subsystem', 'quantity')

class StorageTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

class StorageUnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'storage_type', 'capacity')

class InstalledStorageUnitAdmin(admin.ModelAdmin):
    list_display = ('storage_unit', 'subsystem', 'quantity')  # Removed 'resource', 'currently_stored' as they are now in StoredResource

class StoredResourceAdmin(admin.ModelAdmin):
    list_display = ('storage_unit', 'resource', 'currently_stored')

class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'location_type')

class WorldAdmin(admin.ModelAdmin):
    list_display = ('id','current_tick')

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
