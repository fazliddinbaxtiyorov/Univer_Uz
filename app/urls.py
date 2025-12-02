from django.urls import path
from .views import fanlar_view, reading_test, listening_test

urlpatterns = [
    path('', fanlar_view, name='fanlar'),
    path('reading/', reading_test),
    path('listening/', listening_test)
]
