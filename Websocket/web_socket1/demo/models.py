from django.db import models

# Create your models here.
class Eventinfo(models.Model):
    name = models.CharField(max_length=30, null=True, default='null')
    description = models.CharField(max_length=30, null=True,blank=True, default='无')
    date = models.DateField(blank=True)
    type = models.IntegerField(max_length=2, null=True, default='1')
