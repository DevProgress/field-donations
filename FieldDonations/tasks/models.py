from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

class FieldOffice(models.Model):
    name = models.CharField(max_length=200)  # Make unique
    address = models.CharField(max_length=200) # Make unique
    longitude = models.DecimalField(max_digits=30, decimal_places=25)
    latitude = models.DecimalField(max_digits=30, decimal_places=25)

    def __str__(self):
        return self.name

    def get_coords(self):
        return (self.latitude, self.longitude)

class Person(models.Model):
    user = models.OneToOneField(User)
    email = models.CharField(max_length=200)  # make unique
    name = models.CharField(max_length=200)
    owned_office = models.OneToOneField(FieldOffice, null=True, related_name="owner")
    office = models.ForeignKey(FieldOffice, null=True, related_name="affiliates")

    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=200)
    quantity = models.IntegerField(default=1)
    high_priority = models.BooleanField(default=False)
    details = models.CharField(max_length=200, null=True, blank=True)
    for_office = models.ForeignKey(FieldOffice, on_delete=models.CASCADE)
    added_by = models.ForeignKey(Person, on_delete=models.CASCADE)
    filled = models.BooleanField(default=False)

    def __str__(self):
        return self.name
