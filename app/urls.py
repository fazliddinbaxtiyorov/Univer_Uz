from django.urls import path
from .views import fanlar_view

urlpatterns = [
    path('', fanlar_view, name='fanlar'),
]
