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


class DTM_Practise(models.Model):
    savol = models.TextField()
    variant = models.CharField()
    togri_javob = models.CharField(max_length=1)
    ball = models.IntegerField()
    reyting = models.CharField(max_length=10)


class Students(models.Model):
    ism = models.CharField(max_length=50)
    raqam = models.CharField(max_length=50, default='+998')
    hudud = models.CharField(max_length=120)


