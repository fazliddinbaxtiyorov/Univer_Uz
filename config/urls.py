from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from app.views_lang import set_language

urlpatterns = [
    path("i18n/set-language/", set_language, name="set_language"),
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
    path('', include('user.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)