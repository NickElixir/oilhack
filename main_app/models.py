from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    pass

class Company(models.Model):
    company = models.ForeignKey('self', blank=True, null=True, related_name='children',on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    imp_dep = models.BooleanField(null=True)
    weight = models.IntegerField()
    percent = models.FloatField()

class Project(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    imp_dep = models.BooleanField(null=True)
    weight = models.IntegerField()
    percent = models.FloatField()
"""
class Component(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    base = models.CharField(max_length=50)
    vendor = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    price = models.IntegerField()
    imp_dep = models.BooleanField(null=True)
    weight = models.IntegerField()
    percent = models.FloatField()
"""
