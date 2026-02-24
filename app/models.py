# models.py
from django.db import models
from django.contrib.auth.models import User


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
        ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')
    )
    fan = models.CharField(max_length=30)
    savol = models.TextField()
    savol_rasm = models.ImageField(upload_to='dtm/questions/', blank=True, null=True)
    togri_javob = models.CharField(max_length=1, choices=variant_choise)
    ball = models.FloatField(blank=True, null=True)
    image_a = models.ImageField(upload_to='dtm/variants/', blank=True, null=True)
    image_b = models.ImageField(upload_to='dtm/variants/', blank=True, null=True)
    image_c = models.ImageField(upload_to='dtm/variants/', blank=True, null=True)
    image_d = models.ImageField(upload_to='dtm/variants/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.fan == "birinchi":
            self.ball = 3.1
        elif self.fan == "ikkinchi":
            self.ball = 2.1
        else:
            self.ball = 1.1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.fan} | {self.savol[:30]}"


class IELTS_writing(models.Model):
    text = models.TextField()


class ReadingTest(PaidTestMixin):
    passage_text = models.TextField(verbose_name="Passage matni")
    passage_title = models.CharField(max_length=255, blank=True, default='')
    category = models.CharField(max_length=15, choices=[('READING', 'Reading')], default='READING')

    def __str__(self):
        return f"Reading Test #{self.id} | {self.passage_title[:40]}"


class IELTS_Reading(models.Model):
    QUESTION_TYPES = [
        ('ABCD', 'Multiple Choice'),
        ('TFNG', 'True / False / Not Given'),
        ('MATCH', 'Matching Headings'),
        ('FILL', 'Fill in the Blank'),
    ]

    PART_CHOICES = [
        (1, 'Part 1'),
        (2, 'Part 2'),
        (3, 'Part 3'),
        (4, 'Part 4'),
    ]

    test_group = models.ForeignKey(ReadingTest, on_delete=models.CASCADE, related_name='questions')
    part = models.IntegerField(choices=PART_CHOICES, default=1)  # ✅ YANGI
    savol = models.TextField()
    question_image = models.ImageField(upload_to='reading/questions/', blank=True, null=True)
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPES, default='ABCD')

    variant_a = models.CharField(max_length=255, blank=True)
    variant_b = models.CharField(max_length=255, blank=True)
    variant_c = models.CharField(max_length=255, blank=True)
    variant_d = models.CharField(max_length=255, blank=True)

    image_a = models.ImageField(upload_to='reading/variants/', blank=True, null=True)
    image_b = models.ImageField(upload_to='reading/variants/', blank=True, null=True)
    image_c = models.ImageField(upload_to='reading/variants/', blank=True, null=True)
    image_d = models.ImageField(upload_to='reading/variants/', blank=True, null=True)

    togri_variant = models.CharField(max_length=100)

    def __str__(self):
        return f"Part {self.part} | {self.question_type} | {self.savol[:40]}"

class ListeningTest(PaidTestMixin):
    title = models.CharField(max_length=200)
    description = models.TextField(default="Practice your listening skills.")
    duration = models.IntegerField(default=40)
    category = models.CharField(
        max_length=20,
        choices=[('LISTENING', 'Listening')],
        default='LISTENING'
    )

    def __str__(self):
        return self.title


class IELTSListeningQuestion(models.Model):
    PART_CHOICES = [
        (1, 'Part 1'), (2, 'Part 2'), (3, 'Part 3'), (4, 'Part 4'),
    ]
    QUESTION_TYPES = [
        ('ABCD', 'Multiple Choice'),
        ('FILL', 'Fill in the Blank'),
        ('MATCH', 'Matching'),
        ('MAP', 'Map / Diagram Labelling'),
    ]

    test_group = models.ForeignKey(ListeningTest, on_delete=models.CASCADE, related_name='questions')
    part = models.IntegerField(choices=PART_CHOICES, default=1)
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPES, default='ABCD')
    savol = models.TextField()

    variant_a = models.CharField(max_length=255, blank=True, default='')
    variant_b = models.CharField(max_length=255, blank=True, default='')
    variant_c = models.CharField(max_length=255, blank=True, default='')
    variant_d = models.CharField(max_length=255, blank=True, default='')

    map_image = models.ImageField(upload_to='listening/maps/', blank=True, null=True)

    # ABCD → "A"/"B"/"C"/"D"
    # FILL/MAP → erkin matn
    # MATCH → "A"/"B"/"C"/"D"
    togri_variant = models.CharField(max_length=100)

    audio = models.FileField(upload_to="listening_audio/", blank=True, null=True)

    def __str__(self):
        return f"Part {self.part} | {self.savol[:40]}"


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
    savol_rasm = models.ImageField(upload_to='milliy/questions/', blank=True, null=True)

    variant_a = models.CharField(max_length=255, default='')
    variant_b = models.CharField(max_length=255, default='')
    variant_c = models.CharField(max_length=255, default='')
    variant_d = models.CharField(max_length=255, default='')

    image_a = models.ImageField(upload_to='milliy/variants/', blank=True, null=True)
    image_b = models.ImageField(upload_to='milliy/variants/', blank=True, null=True)
    image_c = models.ImageField(upload_to='milliy/variants/', blank=True, null=True)
    image_d = models.ImageField(upload_to='milliy/variants/', blank=True, null=True)

    togri_variant = models.CharField(
        max_length=1,
        choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')]
    )

    def __str__(self):
        return f"{self.fan} | {self.savol[:30]}"


class Sat(PaidTestMixin):
    title = models.CharField(max_length=200)
    description = models.TextField(default="Practice your SAT skills.")
    duration = models.IntegerField(default=60)
    category = models.CharField(max_length=20, choices=[('SAT', 'SAT')], default='SAT')

    def __str__(self):
        return self.title


class SATQuestion(models.Model):
    QUESTION_TYPES = [
        ('ABCD', 'Multiple Choice'),
        ('TFNG', 'True / False / Not Given'),
    ]
    ANSWER_CHOICES = [("A", "A"), ("B", "B"), ("C", "C"), ("D", "D")]

    test_group = models.ForeignKey(Sat, on_delete=models.CASCADE, related_name='questions')
    savol = models.TextField(verbose_name="Question text")
    question_image = models.ImageField(upload_to='sat/questions/', blank=True, null=True)
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPES, default='ABCD')

    variant_a = models.CharField(max_length=255, blank=True)
    variant_b = models.CharField(max_length=255, blank=True)
    variant_c = models.CharField(max_length=255, blank=True)
    variant_d = models.CharField(max_length=255, blank=True)

    image_a = models.ImageField(upload_to='sat/variants/', blank=True, null=True)
    image_b = models.ImageField(upload_to='sat/variants/', blank=True, null=True)
    image_c = models.ImageField(upload_to='sat/variants/', blank=True, null=True)
    image_d = models.ImageField(upload_to='sat/variants/', blank=True, null=True)

    togri_variant = models.CharField(max_length=1, choices=ANSWER_CHOICES)

    def __str__(self):
        return f"{self.test_group.title} | {self.savol[:40]}"


class Davlat_Univer(models.Model):
    logo = models.ImageField(upload_to='media/')
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text


class Xususiy_Univer(models.Model):
    logo = models.ImageField(upload_to='media/')
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text


class Xorijiy_Univer(models.Model):
    logo = models.ImageField(upload_to='media/')
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject


class UserTestResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test_name = models.CharField(max_length=255)
    score = models.FloatField()
    date_taken = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} | {self.test_name} | {self.score}%"


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
    category = models.CharField(max_length=30, choices=[
        ('IELTS_LISTENING', 'IELTS Listening'),
        ('IELTS_READING', 'IELTS Reading'),
        ('IELTS_WRITING', 'IELTS Writing'),
        ('SAT', 'SAT'),
        ('DTM', 'DTM'),
        ('MILLIY', 'Milliy'),
    ])
    test_id = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'category', 'test_id')

    def __str__(self):
        return f"{self.user.username} | {self.category} | {self.test_id}"