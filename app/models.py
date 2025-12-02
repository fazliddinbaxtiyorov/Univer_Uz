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


class IELTS_writing(models.Model):
    text = models.TextField()


class IELTS_Reading(models.Model):
    savol = models.TextField(default=0)  # Masalan: "2 + 1 = ?"
    variantlar = models.TextField(default=0)  # Masalan: "A 3 B 4 C 5 D 6"
    togri_variant = models.CharField(max_length=1, choices=[('A','A'),('B','B'),('C','C'),('D','D')])

    def __str__(self):
        return self.savol


class IELTSListeningQuestion(models.Model):
    savol = models.TextField()  # Savol matni
    variantlar = models.TextField()  # Masalan: "A 3 B 4 C 5 D 6"
    togri_variant = models.CharField(max_length=1, choices=[('A','A'),('B','B'),('C','C'),('D','D')])
    audio = models.FileField(upload_to='listening_audio/', blank=True, null=True)  # audio fayl

    def __str__(self):
        return self.savol


class Milliy_Sertifikat(models.Model):
    Fan_CHOICES = (
        ('Matematika', 'Matematika'),
        ('Ona Tili', 'Ona Tili'),
        ('Tarix', 'Tarix'),
        ('Kimyo', 'Kimyo'),
        ('Biologiya', 'Biologiya'),
        ('Fizika', 'Fizika'),
        ('Ingliz Tili', 'Ingliz Tili'),
    )

    VARIANT_CHOICES = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
    )

    fan = models.CharField(max_length=20, choices=Fan_CHOICES)
    savol = models.TextField()

    togri_javob = models.TextField()

    togri_variant = models.CharField(max_length=1, choices=VARIANT_CHOICES)

    def __str__(self):
        return f"{self.fan} | {self.savol[:30]}"


from django.db import models


class SATQuestion(models.Model):
    savol = models.TextField()
    variant_a = models.CharField(max_length=255)
    variant_b = models.CharField(max_length=255)
    variant_c = models.CharField(max_length=255)
    variant_d = models.CharField(max_length=255)

    # faqat A/B/C/D saqlaydi
    togri_variant = models.CharField(
        max_length=1,
        choices=[("A","A"),("B","B"),("C","C"),("D","D")]
    )

    def __str__(self):
        return self.savol[:40]
