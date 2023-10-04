from django.db import models

class StorageType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name

class Resource(models.Model):
    name = models.CharField(max_length=100)
    storage_type = models.ForeignKey(StorageType, on_delete=models.CASCADE)

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

    def __str__(self):
        return self.name

class InstalledComponent(models.Model):
    component = models.ForeignKey(Component, related_name='instances', on_delete=models.CASCADE)
    parent_subsystem = models.ForeignKey(SubSystem, related_name='components', on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return self.component.name

class StorageUnit(models.Model):
    name = models.CharField(max_length=100)
    storage_type = models.ForeignKey(StorageType, on_delete=models.CASCADE)
    capacity = models.IntegerField()
    # Add any other fields as needed

    def __str__(self):
        return self.name

class Location(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    location_type = models.CharField(max_length=50)  # This can be 'Star', 'Planet', 'Moon', 'Ship', 'Space Station', 'Surface Installation', etc.
    # ... any other fields like coordinates, description etc.

    def __str__(self):
        return self.name

class InstalledStorageUnit(models.Model):
    storage_unit = models.ForeignKey('StorageUnit', on_delete=models.CASCADE)
    resource = models.ForeignKey('Resource', on_delete=models.CASCADE, null=True, blank=True)
    subsystem = models.ForeignKey('Subsystem', on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField()  # How many units are installed in the subsystem

    def __str__(self):
        return self.storage_unit.name

class StoredResource(models.Model):
    """Defines a resource stored in an installed storage unit."""
    storage_unit = models.ForeignKey('InstalledStorageUnit', related_name='stored_resources', on_delete=models.CASCADE)
    resource = models.ForeignKey('Resource', on_delete=models.CASCADE)
    currently_stored = models.IntegerField()

    def __str__(self):
        return f"{self.resource.name} in {self.storage_unit.storage_unit.name}"
