from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class MeasurementUnit(models.Model):
    name = models.CharField(max_length=200,
                            unique=True)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    measurement_unit = models.ForeignKey(
        MeasurementUnit, on_delete=models.RESTRICT, related_name='ingridients')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Tag(models.Model):
    name = models.CharField(max_length=200)
    color = models.CharField(max_length=7, null=True)
    slug = models.SlugField(max_length=200, null=True, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
