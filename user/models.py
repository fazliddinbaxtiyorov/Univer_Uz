from django.db import models
from django.contrib.auth.models import User

# ======================== USER PROFILE & COINS ========================
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    email = models.EmailField(max_length=254, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    photo = models.ImageField(upload_to='profiles/', blank=True, null=True)
    # Tanga tizimi
    coins = models.PositiveIntegerField(default=0)
    free_trial_used = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.coins} coins"

# ======================== TEST RESULTS & LIMITS ========================
class UserTestResult(models.Model):
    # related_name qo'shildi (applararo to'qnashuvni oldini olish uchun)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='test_results')
    test_name = models.CharField(max_length=255)
    # FieldError'ni yo'qotish uchun test_id qo'shildi
    test_id = models.IntegerField(null=True, blank=True)
    score = models.FloatField()
    # Testni bir marta ishlashni nazorat qilish uchun
    is_completed = models.BooleanField(default=False)
    date_taken = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} | {self.test_name} | {self.score}%"