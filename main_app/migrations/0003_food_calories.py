# Generated by Django 4.0.4 on 2022-05-24 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_food_meal'),
    ]

    operations = [
        migrations.AddField(
            model_name='food',
            name='calories',
            field=models.FloatField(default=0),
        ),
    ]
