from django.contrib import admin
from .models import Resource, ShipSystem, SubSystem, Component, InstalledComponent

class ResourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity')

class ShipSystemAdmin(admin.ModelAdmin):
    list_display = ('name',)

class SubSystemAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent_system')

class ComponentAdmin(admin.ModelAdmin):
    list_display = ('name', 'consumes', 'produces', 'info')

class InstalledComponentAdmin(admin.ModelAdmin):
    list_display = ('component', 'parent_subsystem', 'quantity')

admin.site.register(Resource, ResourceAdmin)
admin.site.register(ShipSystem, ShipSystemAdmin)
admin.site.register(SubSystem, SubSystemAdmin)
admin.site.register(Component, ComponentAdmin)
admin.site.register(InstalledComponent, InstalledComponentAdmin)
