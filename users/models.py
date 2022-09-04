from django.db import models
from django.contrib.auth.models import User

from localflavor.us.models import USStateField, USZipCodeField

class Location(models.Model):
  address_1 = models.CharField(max_length=128)
  address_2 = models.CharField(max_length=128, blank=True)
  city = models.CharField(max_length=64)
  state = USStateField(default='NY')
  zip_code = USZipCodeField(blank=True)

  def __str__(self):
    return f'Location {self.id}'

# Create your models here.
class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  photo = models.ImageField(null=True)
  bio = models.CharField(max_length=140, blank=True)
  phone_number = models.CharField(max_length=12, blank=True)
  location = models.OneToOneField(Location, on_delete=models.CASCADE, null=True)

  def __str__(self):
    return f'{self.user.username}\'s Profile'