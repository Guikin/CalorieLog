# Generated by Django 4.0.4 on 2022-05-24 22:50

# from django.db import migrations

# def insert(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
#     i=0
#     Meals = apps.get_model("main_app", "Meal")
#     for meal in Meals:
#         meal.name = Meals[0][0+i]
#         meal.save()
#         i+=1

# class Migration(migrations.Migration):
#     initial = True

#     dependencies = [
#         ('main_app', '0003_food_calories'),
#     ]

#     operations = [
#         migrations.RunPython(insert)
#     ]
