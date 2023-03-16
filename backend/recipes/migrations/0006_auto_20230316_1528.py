# Generated by Django 3.2.18 on 2023-03-16 12:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0005_auto_20230316_1459'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='favorite',
            name='unique user favorite_recipe',
        ),
        migrations.RemoveField(
            model_name='favorite',
            name='favorite_recipe',
        ),
        migrations.AddField(
            model_name='favorite',
            name='recipe',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='recipe', to='recipes.recipe'),
            preserve_default=False,
        ),
        migrations.AddConstraint(
            model_name='favorite',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='unique user recipe'),
        ),
    ]