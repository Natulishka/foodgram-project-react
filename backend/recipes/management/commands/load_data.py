# python manage.py load_data

import json

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from recipes.models import Ingredient, MeasurementUnit, Tag

User = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **options):

        with open('./data/ingredients.json', 'rb') as f:
            data = json.load(f)
            for line in data:
                measurement_unit, _ = MeasurementUnit.objects.get_or_create(
                    name=line['measurement_unit'])
                Ingredient.objects.get_or_create(
                    name=line['name'].lower(),
                    measurement_unit=measurement_unit)
        print('ingredients finished')

        with open('./data/authors.json', 'rb') as f:
            data = json.load(f)
            for line in data:
                User.objects.create_user(username=line['username'],
                                         email=line['email'],
                                         password=line['password'],
                                         first_name=line['first_name'],
                                         last_name=line['last_name'])
        print('authors finished')

        with open('./data/tags.json', 'rb') as f:
            data = json.load(f)
            for line in data:
                Tag.objects.get_or_create(
                    name=line['name'],
                    color=line['color'],
                    slug=line['slug'])
        print('tags finished')
