from django.db import models

class Resource(models.Model):
    name = models.CharField(max_length=50)
    quantity = models.IntegerField()
