from django.urls import path
from .views import register, Login, profile, setting
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('signup/', register, name='sign'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('settings/', setting, name='settings'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)