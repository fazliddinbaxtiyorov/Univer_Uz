from django.urls import path
from .views import fanlar_view, ielts_listening_view, ielts_reading_view, test_boshlash, fan_tanlash, sat_test_view, ielts, writing
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', fanlar_view, name='fanlar'),
    path('reading/', ielts_reading_view, name='ielts_reading'),
    path('writing', writing, name='writing'),
    path('listening/', ielts_listening_view, name='ielts_listening'),
    path('fan/', fan_tanlash, name='fan_tanlash'),
    path('test/<str:fan>/', test_boshlash, name='test_boshlash'),
    path('sat/', sat_test_view, name='sat_test'),
    path('ielts/', ielts, name='ielts'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
