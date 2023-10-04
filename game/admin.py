from django.contrib import admin
from .models import Resource, ShipSystem, SubSystem, Component, InstalledComponent, StorageType, StorageUnit, InstalledStorageUnit

class ResourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'storage_type', 'quantity')

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
    list_display = ['name', 'storage_type', 'capacity']

class InstalledStorageUnitAdmin(admin.ModelAdmin):
    list_display = ('storage_unit', 'resource', 'currently_stored', 'parent_subsystem', 'quantity')


admin.site.register(Resource, ResourceAdmin)
admin.site.register(ShipSystem, ShipSystemAdmin)
admin.site.register(SubSystem, SubSystemAdmin)
admin.site.register(Component, ComponentAdmin)
admin.site.register(InstalledComponent, InstalledComponentAdmin)
admin.site.register(StorageType)
admin.site.register(StorageUnit)
admin.site.register(InstalledStorageUnit)
