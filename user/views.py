from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from .models import Profile
from .forms import UserRegisterForm
from app.models import UserTestResult
from datetime import date, timedelta
from .models import Friendship


def register(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)

        # ✅ Username band emasligini tekshirish
        username = request.POST.get('username', '').strip()
        if User.objects.filter(username=username).exists():
            messages.error(request, f"'{username}' username allaqachon band! Boshqa username tanlang.")
            return render(request, 'sign.html', {'form': form})

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Siz muvaffaqiyatli ro'yxatdan o'tdingiz!")
            return redirect('/')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    else:
        form = UserRegisterForm()

    return render(request, 'sign.html', {'form': form})


class Login(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')


def upload_photo(request):
    if request.method == "POST":
        profile = request.user.profile
        profile.photo = request.FILES.get("photo")
        profile.save()
    return redirect("my_statistics")


from django.contrib.auth.decorators import login_required


@login_required
def profile(request):
    user = request.user
    user_results = UserTestResult.objects.filter(user=user)
    total_tests_taken = user_results.count()

    if total_tests_taken > 0:
        average_score = round(sum(r.score for r in user_results) / total_tests_taken, 1)
        best_score = max(r.score for r in user_results)
    else:
        average_score = 0
        best_score = 0

    return render(request, 'profile.html', {
        'user': user,
        'total_tests_taken': total_tests_taken,
        'average_score': average_score,
        'best_score': best_score,
        'user_results': user_results,
    })


@login_required
def setting(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)

    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        new_username = request.POST.get('username', '').strip()

        # Username band emasligini tekshirish
        if new_username and new_username != user.username:
            if User.objects.filter(username=new_username).exclude(pk=user.pk).exists():
                messages.error(request, f"'{new_username}' username band! Boshqa nom tanlang.")
                return redirect('settings')

        user.first_name = first_name
        user.last_name = last_name
        if new_username:
            user.username = new_username

        # Parol — faqat yangi parol kiritilsa tekshiriladi
        old_password = request.POST.get('old_password', '').strip()
        new_password = request.POST.get('new_password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()

        if new_password:
            if not old_password:
                messages.error(request, "Eski parolni ham kiriting!")
                return redirect('settings')
            if not user.check_password(old_password):
                messages.error(request, "Eski parol noto'g'ri!")
                return redirect('settings')
            if new_password != confirm_password:
                messages.error(request, "Yangi parollar mos kelmadi!")
                return redirect('settings')
            if len(new_password) < 6:
                messages.error(request, "Parol kamida 6 ta belgi bo'lishi kerak!")
                return redirect('settings')
            user.set_password(new_password)
            messages.success(request, "Parol muvaffaqiyatli o'zgartirildi!")

        profile.email = request.POST.get('email', '').strip()
        profile.phone_number = request.POST.get('phone_number', '').strip()

        if request.FILES.get('photo'):
            profile.photo = request.FILES.get('photo')

        user.save()
        profile.save()

        messages.success(request, "Ma'lumotlar saqlandi ✅")
        return redirect('profile')

    return render(request, 'settings.html', {
        'user': user,
        'profile': profile
    })


# ======================== IELTS BAND SCORE ========================

def score_to_band(correct_count, total=40):
    if total != 40:
        correct_count = round(correct_count * 40 / total)
    table = {
        40: 9.0, 39: 8.5, 38: 8.5, 37: 8.0, 36: 8.0,
        35: 7.5, 34: 7.0, 33: 7.0, 32: 6.5, 31: 6.5,
        30: 6.0, 29: 6.0, 28: 5.5, 27: 5.5, 26: 5.0,
        25: 5.0, 24: 4.5, 23: 4.5, 22: 4.0, 21: 4.0,
        20: 4.0, 19: 3.5, 18: 3.5, 17: 3.0, 16: 3.0,
    }
    return table.get(correct_count, 2.5)


# ======================== STREAK + CHEGIRMA ========================

def update_streak(user):
    profile = user.profile
    today = date.today()
    if profile.last_test_date == today:
        return
    if profile.last_test_date == today - timedelta(days=1):
        profile.streak_days += 1
    else:
        profile.streak_days = 1
    profile.last_test_date = today
    profile.save()


def get_discounted_price(user, original_price):
    if user.profile.streak_days >= 5:
        return int(original_price * 0.75)
    return original_price


# ======================== COINS BACK ========================

def coins_back_if_perfect(user, percentage):
    if percentage == 100.0:
        profile = user.profile
        profile.coins += 20
        profile.save()
        return True
    return False


# ======================== SAT MASTER BADGE ========================

def check_sat_master(user, percentage, test_name):
    if 'SAT' not in test_name:
        return False
    profile = user.profile
    if percentage == 100.0:
        profile.consecutive_perfect += 1
        if profile.consecutive_perfect >= 5:
            profile.badge = 'SAT Master 🏆'
            profile.save()
            return True
    else:
        profile.consecutive_perfect = 0
    profile.save()
    return False