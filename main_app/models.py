from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.forms import CharField
# Create your models here.

# need to attach this to the main model
# user = models.ForeignKey(User, on_delete=models.CASCADE)

# then in shell python manage.py makemigrations > python manage.py migrate

MEALS = (
    ('B', 'Breakfast'),
    ('L', 'Lunch'),
    ('D', 'Dinner'),
    ('S', 'Snack')
)

class Meal(models.Model):
    name=models.CharField(
        max_length = 1,
        choices=MEALS,
        default=MEALS[0][0]
    )


    def __str__(self):
     return f"{self.get_name_display()}"


class Food(models.Model):
    name=models.CharField(max_length=100)
    sugar=models.FloatField(default=0)
    sodium=models.FloatField(default=0)
    fiber=models.FloatField(default=0)
    quantity=models.FloatField(default=0)
    fat=models.FloatField(default=0)
    cholesterol=models.FloatField(default=0)
    protein=models.FloatField(default=0)
    carbohydrates=models.FloatField(default=0)

    def __str__(self):
        return self.name
        
    meal = models.ManyToManyField(Meal)    

class Goals(models.Model):
    calories=models.FloatField(default=0)
    carbs=models.FloatField(default=0)
    fat=models.FloatField(default=0)
    protein=models.FloatField(default=0)
    
    def __str__(self):
        return f"cal={self.calories},carbs={self.carbs},far={self.fat},protein={self.protein}" 
        
        



    




