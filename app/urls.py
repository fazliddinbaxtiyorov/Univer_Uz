from django.urls import path
from .views import fanlar_view, ielts_listening_view, ielts_reading_view, test_boshlash, fan_tanlash, sat_test_view, ielts, writing, univerlar, dtm_test_view, manage_tests, support, contact_view, my_profile_view, test_list_view, ielts_main_dashboard, test_list_sat
from django.conf.urls.static import static
from .views import writing_tests, writing_detail, writing_result, student_analytics, test_list_listening, buy_coins, leaderboard, dtm_select_view, explain_error_view
from django.conf import settings

urlpatterns = [
    path('', fanlar_view, name='home'),
    path('reading/', ielts_reading_view, name='ielts_reading'),
    path('listening/<int:test_id>/', ielts_listening_view, name='ielts_listening'),
    path('listening/', test_list_listening, name='ielts_listening_view'),
    path('fan/', fan_tanlash, name='fan_tanlash'),
    path('test/<str:fan>/', test_boshlash, name='milliy'),
    path('sat_test/<int:test_id>/', sat_test_view, name='sat_test'),
    path('sat/', test_list_sat, name='sat'),
    path('ielts/', ielts_main_dashboard, name='ielts'),
    path('univers/', univerlar, name='univers'),
    path('leaderboard/', leaderboard, name='leaderboard'),
    path('dtm_test/', dtm_test_view, name='dtm_test'),
    path('dtm_select', dtm_select_view, name='selected_subjects'),
    path("tests/", manage_tests, name="manage_tests"),
    path("support/", contact_view, name="support"),
    path("my_statistics/", my_profile_view, name="my_statistics"),
  path('writing/', writing_tests, name='writing_tests'),
  path('writing/<int:pk>/', writing_detail, name='writing_detail'),
  path('result/<int:pk>/', writing_result, name='writing_result'),
  path('analytics/', student_analytics, name='analytics'),
    path('buy_coins/', buy_coins, name='buy_coins'),
    path('explain-error/<int:submission_id>/', explain_error_view, name='explain_error'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
