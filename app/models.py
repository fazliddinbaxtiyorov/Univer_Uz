from django.db import models


# Create your models here.


class Fanlar(models.Model):
    Fan_CHOICES = (
        ('Matematika', 'Matematika'),
        ('Ona Tili', 'Ona Tili'),
        ('Tarix', 'Tarix'),
        ('Kimyo', 'Kimyo'),
        ('Biologiya', 'Biologiya'),
        ('Fizika', 'Fizika'),
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


class IELTS_writing(models.Model):
    text = models.TextField()


class IELTS_Reading(models.Model):
    savol = models.TextField()

    variant_a = models.CharField(max_length=255, default='')
    variant_b = models.CharField(max_length=255, default='')
    variant_c = models.CharField(max_length=255,default='')
    variant_d = models.CharField(max_length=255,default='')

    togri_variant = models.CharField(
        max_length=1,
        choices=[("A", "A"), ("B", "B"), ("C", "C"), ("D", "D")]
    )

    def __str__(self):
        return self.savol[:40]


class IELTSListeningQuestion(models.Model):
    savol = models.TextField()

    variant_a = models.CharField(max_length=255,default='')
    variant_b = models.CharField(max_length=255,default='')
    variant_c = models.CharField(max_length=255,default='')
    variant_d = models.CharField(max_length=255,default='')

    togri_variant = models.CharField(
        max_length=1,
        choices=[("A", "A"), ("B", "B"), ("C", "C"), ("D", "D")]
    )

    audio = models.FileField(
        upload_to="listening_audio/",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.savol[:40]



class Milliy_Sertifikat(models.Model):
    FAN_CHOICES = (
        ('Matematika', 'Matematika'),
        ('Ona Tili', 'Ona Tili'),
        ('Tarix', 'Tarix'),
        ('Kimyo', 'Kimyo'),
        ('Biologiya', 'Biologiya'),
        ('Fizika', 'Fizika'),
        ('Ingliz Tili', 'Ingliz Tili'),
    )

    fan = models.CharField(max_length=20, choices=FAN_CHOICES)
    savol = models.TextField()

    variant_a = models.CharField(max_length=255,default='')
    variant_b = models.CharField(max_length=255,default='')
    variant_c = models.CharField(max_length=255,default='')
    variant_d = models.CharField(max_length=255,default='')

    # faqat A / B / C / D
    togri_variant = models.CharField(
        max_length=1,
        choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')]
    )

    def __str__(self):
        return f"{self.fan} | {self.savol[:30]}"


class SATQuestion(models.Model):
    savol = models.TextField()
    variant_a = models.CharField(max_length=255)
    variant_b = models.CharField(max_length=255)
    variant_c = models.CharField(max_length=255)
    variant_d = models.CharField(max_length=255)

    togri_variant = models.CharField(
        max_length=1,
        choices=[("A","A"),("B","B"),("C","C"),("D","D")]
    )

    def __str__(self):
        return self.savol[:40]


class Davlat_Univer(models.Model):
    logo = models.ImageField(upload_to='media/')
    text = models.CharField(max_length=255)


class Xususiy_Univer(models.Model):
    logo = models.ImageField(upload_to='media/')
    text = models.CharField(max_length=255)


class Xorijiy_Univer(models.Model):
    logo = models.ImageField(upload_to='media/')
    text = models.CharField(max_length=255)

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject

from django.contrib.auth.models import User
from django.db import models

class UserTestResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test_name = models.CharField(max_length=255)
    score = models.FloatField()   # masalan: 0-100%
    date_taken = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} | {self.test_name} | {self.score}%"
