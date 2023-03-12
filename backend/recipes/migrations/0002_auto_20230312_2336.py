# Generated by Django 3.2.18 on 2023-03-12 20:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('color', models.CharField(max_length=7, null=True)),
                ('slug', models.SlugField(max_length=200, null=True, unique=True)),
            ],
        ),
        migrations.AlterField(
            model_name='measurementunit',
            name='name',
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.DeleteModel(
            name='Ingredients',
        ),
        migrations.AddField(
            model_name='ingredient',
            name='measurement_unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='ingridients', to='recipes.measurementunit'),
        ),
    ]
