from django.db import models


# Create your models here.

class PaidTestMixin(models.Model):
    is_paid = models.BooleanField(default=False)
    price = models.PositiveIntegerField(default=25)

    class Meta:
        abstract = True

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



class ReadingTest(PaidTestMixin):
    passage_text = models.TextField(verbose_name="Test matni (Passage)")
    category = models.CharField(
        max_length=15,
        choices=[('READING', 'Reading')],
        default='READING'
    )

class IELTS_Reading(models.Model):

    QUESTION_TYPES = [
        ('ABCD', 'Multiple Choice'),
        ('TFNG', 'True / False / Not Given'),
    ]

    ANSWER_CHOICES = [
        ("A", "A"),
        ("B", "B"),
        ("C", "C"),
        ("D", "D"),
    ]

    test_group = models.ForeignKey(
        ReadingTest,
        on_delete=models.CASCADE,
        related_name='questions'
    )

    savol = models.TextField()
    question_image = models.ImageField(
        upload_to='reading/questions/',
        blank=True,
        null=True
    )

    question_type = models.CharField(
        max_length=10,
        choices=QUESTION_TYPES,
        default='ABCD'
    )

    variant_a = models.CharField(max_length=255, blank=True)
    variant_b = models.CharField(max_length=255, blank=True)
    variant_c = models.CharField(max_length=255, blank=True)
    variant_d = models.CharField(max_length=255, blank=True)

    image_a = models.ImageField(upload_to='reading/variants/', blank=True, null=True)
    image_b = models.ImageField(upload_to='reading/variants/', blank=True, null=True)
    image_c = models.ImageField(upload_to='reading/variants/', blank=True, null=True)
    image_d = models.ImageField(upload_to='reading/variants/', blank=True, null=True)

    togri_variant = models.CharField(
        max_length=1,
        choices=ANSWER_CHOICES
    )

    def __str__(self):
        return f"{self.question_type} | {self.savol[:40]}"

class ListeningTest(PaidTestMixin):
    title = models.CharField(max_length=200)
    description = models.TextField(default="Practice your reading skills.")
    duration = models.IntegerField(default=60)
    category = models.CharField(max_length=20, choices=[('READING', 'Reading'), ('LISTENING', 'Listening')])

    def __str__(self):
        return self.title

class IELTSListeningQuestion(models.Model):
    test_group = models.ForeignKey(ListeningTest, on_delete=models.CASCADE, related_name='questions')
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



class Milliy_Sertifikat(PaidTestMixin):
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

class Sat(PaidTestMixin):
    title = models.CharField(max_length=200)
    description = models.TextField(default="Practice your sat skills.")
    duration = models.IntegerField(default=60)
    category = models.CharField(max_length=20, choices=[('SAT', 'SAT')])

class SATQuestion(models.Model):
    test_group = models.ForeignKey(Sat, on_delete=models.CASCADE, related_name='questions')
    QUESTION_TYPES = [
        ('ABCD', 'Multiple Choice'),
        ('TFNG', 'True / False / Not Given'),
    ]

    ANSWER_CHOICES = [
        ("A", "A"),
        ("B", "B"),
        ("C", "C"),
        ("D", "D"),
    ]

    test_group = models.ForeignKey(
        Sat,
        on_delete=models.CASCADE,
        related_name='questions'
    )

    savol = models.TextField(verbose_name="Question text")
    question_image = models.ImageField(
        upload_to='sat/questions/',
        blank=True,
        null=True
    )

    question_type = models.CharField(
        max_length=10,
        choices=QUESTION_TYPES,
        default='ABCD'
    )

    # Variantlar matni
    variant_a = models.CharField(max_length=255, blank=True)
    variant_b = models.CharField(max_length=255, blank=True)
    variant_c = models.CharField(max_length=255, blank=True)
    variant_d = models.CharField(max_length=255, blank=True)

    # Variantlar rasm ko‘rinishida ham bo‘lishi mumkin
    image_a = models.ImageField(upload_to='sat/variants/', blank=True, null=True)
    image_b = models.ImageField(upload_to='sat/variants/', blank=True, null=True)
    image_c = models.ImageField(upload_to='sat/variants/', blank=True, null=True)
    image_d = models.ImageField(upload_to='sat/variants/', blank=True, null=True)

    # Tog'ri javob
    togri_variant = models.CharField(
        max_length=1,
        choices=ANSWER_CHOICES
    )

    def __str__(self):
        return f"{self.test_group.title} | {self.savol[:40]}"



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

from django.db import models
from django.contrib.auth.models import User

class WritingQuestion(PaidTestMixin):
    TASK_CHOICES = (
        ('task1', 'Task 1'),
        ('task2', 'Task 2'),
    )

    title = models.CharField(max_length=255)
    task_type = models.CharField(max_length=10, choices=TASK_CHOICES)
    question_text = models.TextField()
    question_image = models.ImageField(upload_to='writing/question/', blank=True, null=True)

    def __str__(self):
        return self.title


class WritingSubmission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(WritingQuestion, on_delete=models.CASCADE)

    answer = models.TextField()

    band_score = models.FloatField(null=True, blank=True)
    feedback = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.question.title}"

class TestAccess(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    category = models.CharField(
        max_length=30,
        choices=[
            ('IELTS_LISTENING', 'IELTS Listening'),
            ('IELTS_READING', 'IELTS Reading'),
            ('IELTS_WRITING', 'IELTS Writing'),

            ('SAT', 'SAT'),
            ('DTM', 'DTM'),
            ('MILLIY', 'Milliy'),
        ]
    )

    test_id = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'category', 'test_id')
