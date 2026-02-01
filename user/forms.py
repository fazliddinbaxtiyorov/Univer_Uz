from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Email'}))
    phone_number = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Phone Number'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number','password1', 'password2']
        help_texts = {
            'username': None,
            'password1': None,
            'password2': None,
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Profile yaratish
            Profile.objects.create(
                user=user,
                email=self.cleaned_data['email'],
                phone_number=self.cleaned_data['phone_number'],
            )
        return user
