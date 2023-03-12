from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class MeasurementUnit(models.Model):
    namr = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name


class Ingredients(models.Model):
    name = models.CharField(max_length=256)
    measurement_unit = models.ForeignKey(
        MeasurementUnit, on_delete=models.RESTRICT, related_name='ingridients')

    def __str__(self):
        return self.name
    