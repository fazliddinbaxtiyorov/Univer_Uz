from django.urls import path
from .views import fanlar_view, ielts_listening_view, ielts_reading_view, test_boshlash, fan_tanlash, sat_test_view, ielts, writing, univerlar, davlat_univer, xorijiy_univer, xususiy_univer, dtm_test_view, manage_tests, support, contact_view, my_profile_view
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', fanlar_view, name='home'),
    path('reading/', ielts_reading_view, name='ielts_reading'),
    path('writing', writing, name='writing'),
    path('listening/', ielts_listening_view, name='ielts_listening'),
    path('fan/', fan_tanlash, name='fan_tanlash'),
    path('test/<str:fan>/', test_boshlash, name='milliy'),
    path('sat/', sat_test_view, name='sat'),
    path('ielts/', ielts, name='ielts'),
    path('univers/', univerlar, name='univers'),
    path('davlat_univers/', davlat_univer, name='davlat_univer'),
    path('xususiy_univers/', xususiy_univer, name='xususiy_univer'),
    path('xorijiy_univers/', xorijiy_univer, name='xorijiy_univer'),
    path('dtm_test/', dtm_test_view, name='dtm_test'),
    path("tests/", manage_tests, name="manage_tests"),
    path("support/", contact_view, name="support"),
    path("my_statistics/", my_profile_view, name="my_statistics"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
