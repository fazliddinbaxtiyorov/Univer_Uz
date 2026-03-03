from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class PaidTestMixin(models.Model):
    is_paid = models.BooleanField(default=False)
    price = models.PositiveIntegerField(default=25)
    class Meta:
        abstract = True


class Fanlar(models.Model):
    Fan_CHOICES = (
        ('Matematika','Matematika'),('Ona Tili','Ona Tili'),('Tarix','Tarix'),
        ('Kimyo','Kimyo'),('Biologiya','Biologiya'),('Fizika','Fizika'),('Ingliz Tili','Ingliz Tili'),
    )
    birinchi_fan     = models.CharField(max_length=30, choices=Fan_CHOICES)
    ikkinchi_fan     = models.CharField(max_length=30, choices=Fan_CHOICES)
    uchinchi_fan     = models.CharField(max_length=30, default='Ona Tili')
    tortinchi_fan    = models.CharField(max_length=30, default='Matematika')
    beshinchichi_fan = models.CharField(max_length=20, default='Tarix')


class DTM_Practise(models.Model):
    variant_choise = (('A','A'),('B','B'),('C','C'),('D','D'))
    fan        = models.CharField(max_length=30)
    savol      = models.TextField()
    savol_rasm = models.ImageField(upload_to='dtm/questions/', blank=True, null=True)
    togri_javob = models.CharField(max_length=1, choices=variant_choise)
    ball       = models.FloatField(blank=True, null=True)
    image_a    = models.ImageField(upload_to='dtm/variants/', blank=True, null=True)
    image_b    = models.ImageField(upload_to='dtm/variants/', blank=True, null=True)
    image_c    = models.ImageField(upload_to='dtm/variants/', blank=True, null=True)
    image_d    = models.ImageField(upload_to='dtm/variants/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.fan == "birinchi": self.ball = 3.1
        elif self.fan == "ikkinchi": self.ball = 2.1
        else: self.ball = 1.1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.fan} | {self.savol[:30]}"


class IELTS_writing(models.Model):
    text = models.TextField()


class ReadingTest(PaidTestMixin):
    passage_title   = models.CharField(max_length=255, blank=True, default='')
    passage_text    = models.TextField(verbose_name="Passage 1 matni")
    passage_title_2 = models.CharField(max_length=255, blank=True, default='', verbose_name="Passage 2 sarlavha")
    passage_text_2  = models.TextField(blank=True, default='', verbose_name="Passage 2 matni")
    passage_title_3 = models.CharField(max_length=255, blank=True, default='', verbose_name="Passage 3 sarlavha")
    passage_text_3  = models.TextField(blank=True, default='', verbose_name="Passage 3 matni")
    category = models.CharField(max_length=15, choices=[('READING','Reading')], default='READING')

    def get_passage(self, part_num):
        return {
            1: (self.passage_title,   self.passage_text),
            2: (self.passage_title_2, self.passage_text_2),
            3: (self.passage_title_3, self.passage_text_3),
        }.get(part_num, ('', ''))

    def __str__(self):
        return f"Reading Test #{self.id} | {self.passage_title[:40]}"


class IELTS_Reading(models.Model):
    QUESTION_TYPES = [
        ('ABCD',    'Multiple Choice'),
        ('TFNG',    'True / False / Not Given'),
        ('YNNG',    'Yes / No / Not Given'),
        ('MATCH',   'Matching Headings'),
        ('FILL',    'Fill in the Blank'),
        ('FILLBOX', 'Fill in the Blank with Word Box'),
    ]
    PART_CHOICES = [
        (1,'Part 1'),(2,'Part 2'),(3,'Part 3'),(4,'Part 4'),
    ]

    test_group     = models.ForeignKey(ReadingTest, on_delete=models.CASCADE, related_name='questions')
    part           = models.IntegerField(choices=PART_CHOICES, default=1)
    savol          = models.TextField()
    question_image = models.ImageField(upload_to='reading/questions/', blank=True, null=True)
    question_type  = models.CharField(max_length=10, choices=QUESTION_TYPES, default='ABCD')

    # ABCD / MATCH asosiy 4 ta variant (MATCH da i–iv headinglar)
    variant_a = models.CharField(max_length=500, blank=True)
    variant_b = models.CharField(max_length=500, blank=True)
    variant_c = models.CharField(max_length=500, blank=True)
    variant_d = models.CharField(max_length=500, blank=True)

    # MATCH qo'shimcha headinglar (v–xii)
    variant_e = models.CharField(max_length=500, blank=True, verbose_name="Heading v")
    variant_f = models.CharField(max_length=500, blank=True, verbose_name="Heading vi")
    variant_g = models.CharField(max_length=500, blank=True, verbose_name="Heading vii")
    variant_h = models.CharField(max_length=500, blank=True, verbose_name="Heading viii")
    variant_i = models.CharField(max_length=500, blank=True, verbose_name="Heading ix")
    variant_j = models.CharField(max_length=500, blank=True, verbose_name="Heading x")
    variant_k = models.CharField(max_length=500, blank=True, verbose_name="Heading xi")
    variant_l = models.CharField(max_length=500, blank=True, verbose_name="Heading xii")

    # ABCD rasm variantlar
    image_a = models.ImageField(upload_to='reading/variants/', blank=True, null=True)
    image_b = models.ImageField(upload_to='reading/variants/', blank=True, null=True)
    image_c = models.ImageField(upload_to='reading/variants/', blank=True, null=True)
    image_d = models.ImageField(upload_to='reading/variants/', blank=True, null=True)

    # FILLBOX — so'zlar qutisi (vergul bilan ajratilgan)
    word_box = models.TextField(
        blank=True, default='',
        verbose_name="Word Box (vergul bilan ajrating)",
        help_text="Faqat FILLBOX turida. Masalan: Mexicans,random,rotating,despite,preserve"
    )

    # togri_variant:
    # ABCD/MATCH → "A" / "xi"
    # TFNG → "TRUE" / "FALSE" / "NOT GIVEN"
    # YNNG → "YES" / "NO" / "NOT GIVEN"
    # FILL → erkin matn
    # FILLBOX → vergul bilan: "preserve,realising,friction,rotating,Eskimos,despite"
    togri_variant = models.CharField(max_length=1000)

    def get_word_box_list(self):
        if not self.word_box:
            return []
        return [w.strip() for w in self.word_box.split(',') if w.strip()]

    def get_correct_list(self):
        """FILLBOX uchun to'g'ri javoblar listi"""
        if not self.togri_variant:
            return []
        return [a.strip().lower() for a in self.togri_variant.split(',') if a.strip()]

    def __str__(self):
        return f"Part {self.part} | {self.question_type} | {self.savol[:40]}"


class ListeningTest(PaidTestMixin):
    title       = models.CharField(max_length=200)
    description = models.TextField(default="Practice your listening skills.")
    duration    = models.IntegerField(default=40)
    category    = models.CharField(max_length=20, choices=[('LISTENING','Listening')], default='LISTENING')

    def __str__(self):
        return self.title


class IELTSListeningQuestion(models.Model):
    PART_CHOICES   = [(1,'Part 1'),(2,'Part 2'),(3,'Part 3'),(4,'Part 4')]
    QUESTION_TYPES = [
        ('ABCD',  'Multiple Choice'),
        ('FILL',  'Fill in the Blank'),
        ('MATCH', 'Matching'),
        ('MAP',   'Map / Diagram / Image'),
        ('CHECK', 'Checkbox (Multiple Select)'),  # ← YANGI
    ]
    test_group    = models.ForeignKey(ListeningTest, on_delete=models.CASCADE, related_name='questions')
    part          = models.IntegerField(choices=PART_CHOICES, default=1)
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPES, default='ABCD')
    savol         = models.TextField()

    # ABCD / MATCH / CHECK variantlari
    variant_a = models.CharField(max_length=255, blank=True, default='')
    variant_b = models.CharField(max_length=255, blank=True, default='')
    variant_c = models.CharField(max_length=255, blank=True, default='')
    variant_d = models.CharField(max_length=255, blank=True, default='')
    variant_e = models.CharField(max_length=255, blank=True, default='', verbose_name="Variant E")
    variant_f = models.CharField(max_length=255, blank=True, default='', verbose_name="Variant F")
    variant_g = models.CharField(max_length=255, blank=True, default='', verbose_name="Variant G")
    variant_h = models.CharField(max_length=255, blank=True, default='', verbose_name="Variant H")
    variant_i = models.CharField(max_length=255, blank=True, default='', verbose_name="Variant I")

    map_image     = models.ImageField(upload_to='listening/maps/', blank=True, null=True)
    togri_variant = models.CharField(
        max_length=200,
        help_text="ABCD → 'A'; CHECK → 'A,C,F' (vergul bilan); FILL → erkin matn"
    )
    audio = models.FileField(upload_to="listening_audio/", blank=True, null=True)

    def get_correct_list(self):
        """CHECK uchun to'g'ri javoblar listi"""
        return [x.strip().upper() for x in self.togri_variant.split(',') if x.strip()]

    def __str__(self):
        return f"Part {self.part} | {self.question_type} | {self.savol[:40]}"

class Milliy_Sertifikat(models.Model):
    FAN_CHOICES = (
        ('Matematika','Matematika'),('Ona Tili','Ona Tili'),('Tarix','Tarix'),
        ('Kimyo','Kimyo'),('Biologiya','Biologiya'),('Fizika','Fizika'),('Ingliz Tili','Ingliz Tili'),
    )
    fan        = models.CharField(max_length=20, choices=FAN_CHOICES)
    savol      = models.TextField()
    savol_rasm = models.ImageField(upload_to='milliy/questions/', blank=True, null=True)
    variant_a  = models.CharField(max_length=255, default='')
    variant_b  = models.CharField(max_length=255, default='')
    variant_c  = models.CharField(max_length=255, default='')
    variant_d  = models.CharField(max_length=255, default='')
    image_a    = models.ImageField(upload_to='milliy/variants/', blank=True, null=True)
    image_b    = models.ImageField(upload_to='milliy/variants/', blank=True, null=True)
    image_c    = models.ImageField(upload_to='milliy/variants/', blank=True, null=True)
    image_d    = models.ImageField(upload_to='milliy/variants/', blank=True, null=True)
    togri_variant = models.CharField(max_length=1, choices=[('A','A'),('B','B'),('C','C'),('D','D')])

    def __str__(self):
        return f"{self.fan} | {self.savol[:30]}"


class Sat(PaidTestMixin):
    title       = models.CharField(max_length=200)
    description = models.TextField(default="Practice your SAT skills.")
    duration    = models.IntegerField(default=60)
    category    = models.CharField(max_length=20, choices=[('SAT','SAT')], default='SAT')

    def __str__(self):
        return self.title


class DTM_Majburiy(models.Model):
    FAN_CHOICES = (('Ona Tili','Ona Tili'),('Matematika','Matematika'),('Tarix','Tarix'))
    fan        = models.CharField(max_length=20, choices=FAN_CHOICES)
    savol      = models.TextField()
    savol_rasm = models.ImageField(upload_to='dtm_majburiy/questions/', blank=True, null=True)
    variant_a  = models.CharField(max_length=255, default='')
    variant_b  = models.CharField(max_length=255, default='')
    variant_c  = models.CharField(max_length=255, default='')
    variant_d  = models.CharField(max_length=255, default='')
    image_a    = models.ImageField(upload_to='dtm_majburiy/variants/', blank=True, null=True)
    image_b    = models.ImageField(upload_to='dtm_majburiy/variants/', blank=True, null=True)
    image_c    = models.ImageField(upload_to='dtm_majburiy/variants/', blank=True, null=True)
    image_d    = models.ImageField(upload_to='dtm_majburiy/variants/', blank=True, null=True)
    togri_variant = models.CharField(max_length=1, choices=[('A','A'),('B','B'),('C','C'),('D','D')])

    def __str__(self):
        return f"{self.fan} | {self.savol[:30]}"


class SATQuestion(models.Model):
    QUESTION_TYPES = [('ABCD','Multiple Choice'),('TFNG','True / False / Not Given')]
    ANSWER_CHOICES = [("A","A"),("B","B"),("C","C"),("D","D")]
    test_group     = models.ForeignKey(Sat, on_delete=models.CASCADE, related_name='questions')
    savol          = models.TextField(verbose_name="Question text")
    question_image = models.ImageField(upload_to='sat/questions/', blank=True, null=True)
    question_type  = models.CharField(max_length=10, choices=QUESTION_TYPES, default='ABCD')
    variant_a      = models.CharField(max_length=255, blank=True)
    variant_b      = models.CharField(max_length=255, blank=True)
    variant_c      = models.CharField(max_length=255, blank=True)
    variant_d      = models.CharField(max_length=255, blank=True)
    image_a        = models.ImageField(upload_to='sat/variants/', blank=True, null=True)
    image_b        = models.ImageField(upload_to='sat/variants/', blank=True, null=True)
    image_c        = models.ImageField(upload_to='sat/variants/', blank=True, null=True)
    image_d        = models.ImageField(upload_to='sat/variants/', blank=True, null=True)
    togri_variant  = models.CharField(max_length=1, choices=ANSWER_CHOICES)

    def __str__(self):
        return f"{self.test_group.title} | {self.savol[:40]}"


class Davlat_Univer(models.Model):
    logo = models.ImageField(upload_to='media/')
    text = models.CharField(max_length=255)
    def __str__(self): return self.text

class Xususiy_Univer(models.Model):
    logo = models.ImageField(upload_to='media/')
    text = models.CharField(max_length=255)
    def __str__(self): return self.text

class Xorijiy_Univer(models.Model):
    logo = models.ImageField(upload_to='media/')
    text = models.CharField(max_length=255)
    def __str__(self): return self.text


class ContactMessage(models.Model):
    name       = models.CharField(max_length=100)
    email      = models.EmailField()
    subject    = models.CharField(max_length=200)
    message    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.subject


class UserTestResult(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    test_name  = models.CharField(max_length=255)
    score      = models.FloatField()
    date_taken = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"{self.user.username} | {self.test_name} | {self.score}%"


class WritingQuestion(PaidTestMixin):
    TASK_CHOICES   = (('task1','Task 1'),('task2','Task 2'))
    title          = models.CharField(max_length=255)
    task_type      = models.CharField(max_length=10, choices=TASK_CHOICES)
    question_text  = models.TextField()
    question_image = models.ImageField(upload_to='writing/question/', blank=True, null=True)
    def __str__(self): return self.title


class WritingSubmission(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    question   = models.ForeignKey(WritingQuestion, on_delete=models.CASCADE)
    answer     = models.TextField()
    band_score = models.FloatField(null=True, blank=True)
    feedback   = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"{self.user.username} - {self.question.title}"


class TestAccess(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    category   = models.CharField(max_length=30, choices=[
        ('IELTS_LISTENING','IELTS Listening'),('IELTS_READING','IELTS Reading'),
        ('IELTS_WRITING','IELTS Writing'),('SAT','SAT'),('DTM','DTM'),('MILLIY','Milliy'),
    ])
    test_id    = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    paid       = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user','category','test_id')

    def __str__(self):
        return f"{self.user.username} | {self.category} | {self.test_id}"


class News(models.Model):
    title      = models.CharField(max_length=300)
    slug       = models.SlugField(unique=True, blank=True)
    category   = models.CharField(max_length=100, blank=True)
    excerpt    = models.TextField(blank=True)
    content    = models.TextField()
    image      = models.ImageField(upload_to='news/', blank=True, null=True)
    is_active  = models.BooleanField(default=True)
    is_new     = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)