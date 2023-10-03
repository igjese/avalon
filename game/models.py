from django.db import models

class Resource(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()

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

    def __str__(self):
        return self.name

class InstalledComponent(models.Model):
    component = models.ForeignKey(Component, related_name='instances', on_delete=models.CASCADE)
    parent_subsystem = models.ForeignKey(SubSystem, related_name='components', on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return self.component.name
