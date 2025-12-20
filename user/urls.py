from django.urls import path
from .views import register, Login, profile
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/', register, name='sign'),
    path('profile/', profile, name='profile'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
]