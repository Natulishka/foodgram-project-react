# python manage.py load_data

import json

from django.core.management.base import BaseCommand

from recipes.models import Ingredient, MeasurementUnit


class Command(BaseCommand):
    def handle(self, *args, **options):

        with open('./../data/ingredients.json', 'rb') as f:
            data = json.load(f)
            for line in data:
                measurement_unit, _ = MeasurementUnit.objects.get_or_create(
                    name=line['measurement_unit'])
                Ingredient.objects.get_or_create(
                    name=line['name'].lower(),
                    measurement_unit=measurement_unit)
        print('finished')
