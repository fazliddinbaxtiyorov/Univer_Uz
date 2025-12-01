from django.db import models


# Create your models here.


class Fanlar(models.Model):
    Fan_CHOICES = (
        ('Matematika', 'Matematika'),
        ('Ona Tili', 'Ona Tili'),
        ('Tarix', 'Tarix'),
        ('Kimyo', 'Kimyo'),
        ('Biologiya', 'Biologiya'),
        ('Geografiya', 'Geografiya'),
        ('Fizika', 'Fiziki'),
        ('Ingliz Tili', 'Ingliz Tili'),
    )
    birinchi_fan = models.CharField(max_length=30, choices=Fan_CHOICES)
    ikkinchi_fan = models.CharField(max_length=30, choices=Fan_CHOICES)
    uchinchi_fan = models.CharField(max_length=30, default='Ona Tili')
    tortinchi_fan = models.CharField(max_length=30, default='Matematika')
    beshinchichi_fan = models.CharField(max_length=20, default='Tarix')


class DTM_Practise(models.Model):
    variant_choise = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D')
    )
    fan = models.CharField(max_length=30)
    savol = models.TextField()
    togri_javob = models.CharField(max_length=1, choices=variant_choise)
    ball = models.FloatField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.fan == "birinchi":
            self.ball = 3.1
        elif self.fan == "ikkinchi":
            self.ball = 2.1
        else:
            self.ball = 1.1

        super().save(*args, **kwargs)


class Students(models.Model):
    ism = models.CharField(max_length=50)
    raqam = models.CharField(max_length=50, default='+998')
    hudud = models.CharField(max_length=120)
