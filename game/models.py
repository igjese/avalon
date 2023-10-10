from django.db import models
import jsonfield  # You'll need to install this package

class World(models.Model):
    current_tick = models.IntegerField(default=0)

class ResourceHistory(models.Model):
    tick = models.IntegerField()
    quantity_data = jsonfield.JSONField(default=dict)  # Stores the resource quantity data as JSON
    production_data = jsonfield.JSONField(default=dict)  # Stores the aggregated production data as JSON
    consumption_data = jsonfield.JSONField(default=dict)  # Stores the aggregated consumption data as JSON

class StorageType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    info = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Resource(models.Model):
    name = models.CharField(max_length=100)
    storage_type = models.ForeignKey(StorageType, related_name='resources', on_delete=models.CASCADE)
    info = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class ShipSystem(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class SubSystem(models.Model):
    name = models.CharField(max_length=100)
    parent_system = models.ForeignKey(ShipSystem, related_name='subsystems', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Component(models.Model):
    name = models.CharField(max_length=100)
    consumes = models.JSONField(default=dict, blank=True, null=True)  # e.g., {"Energy": 1, "Food": 1, "Water": 1}
    produces = models.JSONField(default=dict, blank=True, null=True)  # e.g., {"Oxygen": 1}
    info = models.CharField(max_length=100)
    ticks_per_cycle = models.IntegerField(default=1)  # Number of ticks required for one cycle

    def __str__(self):
        return self.name

COMPONENT_STATES = [
    ('INTAKE', 'Waiting for resources'),
    ('WORKING', 'Working'),
    ('OUTPUT', 'Waiting to output'),
]
class InstalledComponent(models.Model):
    component = models.ForeignKey(Component, related_name='instances', on_delete=models.CASCADE)
    parent_subsystem = models.ForeignKey(SubSystem, related_name='components', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    remaining_ticks_for_cycle = models.IntegerField(default=0)  # Remaining ticks for the current cycle
    state = models.CharField(max_length=30, choices=COMPONENT_STATES, default='INTAKE')
    input_buffer = models.JSONField(default=dict, blank=True, null=True)
    output_buffer = models.JSONField(default=dict, blank=True, null=True)

    def __str__(self):
        return self.component.name

class StorageUnit(models.Model):
    name = models.CharField(max_length=100)
    storage_type = models.ForeignKey(StorageType, related_name='storage_units', on_delete=models.CASCADE)
    capacity = models.IntegerField()
    info = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Location(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    location_type = models.CharField(max_length=50)  # This can be 'Star', 'Planet', 'Moon', 'Ship', 'Space Station', 'Surface Installation', etc.

    def __str__(self):
        return self.name

class InstalledStorageUnit(models.Model):
    storage_unit = models.ForeignKey('StorageUnit', on_delete=models.CASCADE)
    assigned_resource = models.ForeignKey('Resource', related_name='assigned_storage_unit', on_delete=models.CASCADE, null=True, blank=True)
    subsystem = models.ForeignKey('Subsystem', related_name='installed_storage_units', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.storage_unit.name

class StoredResource(models.Model):
    """Defines a resource stored in an installed storage unit."""
    storage_unit = models.ForeignKey('InstalledStorageUnit', related_name='stored_resources', on_delete=models.CASCADE)
    resource = models.ForeignKey('Resource', related_name='stored_resources', on_delete=models.CASCADE)
    currently_stored = models.IntegerField()

    def __str__(self):
        return f"{self.resource.name} in {self.storage_unit.storage_unit.name}"
