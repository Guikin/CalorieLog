from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# need to attach this to the main model
# user = models.ForeignKey(User, on_delete=models.CASCADE)

# then in shell python manage.py makemigrations > python manage.py migrate