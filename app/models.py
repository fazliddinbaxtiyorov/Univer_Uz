from django.db import models

# Create your models here.


class Fanlar(models.Model):
    birinchi_fan = models.CharField(max_length=120)
    ikkinchi_fan = models.CharField(max_length=120)
    uchinchi_fan = models.CharField(max_length=120)
    tortinchi_fan = models.CharField(max_length=120)
    beshinchichi_fan = models.CharField(max_length=120)
    oltinchi_fan = models.CharField(max_length=120)
    yettinchi_fan = models.CharField(max_length=120)
    sakkizinchi_fan = models.CharField(max_length=120)

