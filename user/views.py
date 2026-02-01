from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from .models import Profile
from .forms import UserRegisterForm
from app.models import UserTestResult
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import UserRegisterForm

def register(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Siz muvaffaqiyatli ro‘yxatdan o‘tdingiz!')
            return redirect('/')
    else:
        form = UserRegisterForm()

    return render(request, 'sign.html', {'form': form})

class Login(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')


def profile(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('profile')
    else:
        form = UserRegisterForm()
    user = request.user

    user_results = UserTestResult.objects.filter(user=user)

    total_tests_taken = user_results.count()

    if total_tests_taken > 0:
        average_score = round(sum(result.score for result in user_results) / total_tests_taken, 1)
        best_score = max(result.score for result in user_results)
    else:
        average_score = 0
        best_score = 0

    return render(request, 'profile.html', {'form': form, 'user': user.get_full_name() or user.username,
        'total_tests_taken': total_tests_taken,
        'average_score': average_score,
        'best_score': best_score,
        'user_results': user_results, })

# views.py
def upload_photo(request):
    if request.method == "POST":
        profile = request.user.profile
        profile.photo = request.FILES.get("photo")
        profile.save()
    return redirect("profile")
