from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy


from .forms import UserRegisterForm


def register(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
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
        return reverse_lazy('fanlar')


def profile(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        username = form.cleaned_data.get('username')
        return render(request, 'profile.html', {'user': username})
    else:
        form = UserRegisterForm()
        return render(request, 'profile.html', {'form': form})