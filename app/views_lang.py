# core/views_lang.py
# Foydalanuvchi til tanlaganda shu view chaqiriladi

from django.http                    import JsonResponse
from django.utils                   import translation
from django.utils.translation       import check_for_language
from django.views.decorators.http   import require_POST
from django.views.decorators.csrf   import csrf_exempt
from django.conf                    import settings
import json


@csrf_exempt
@require_POST
def set_language(request):
    """
    POST /i18n/set-language/
    Body: {"lang": "ru"}

    Session + cookie ga saqlaydi, Django middleware keyingi
    har bir so'rovda tilni avtomatik o'rnatadi.
    """
    try:
        body = json.loads(request.body)
        lang = body.get("lang", "en")
    except (json.JSONDecodeError, AttributeError):
        lang = request.POST.get("language", "en")

    if not check_for_language(lang):
        return JsonResponse({"error": f"Unsupported language: {lang}"}, status=400)

    # Django 4.x da LANGUAGE_SESSION_KEY olib tashlangan
    translation.activate(lang)
    request.session[settings.LANGUAGE_COOKIE_NAME] = lang  # ✅ to'g'ri yo'l

    response = JsonResponse({"ok": True, "lang": lang})
    response.set_cookie(
        settings.LANGUAGE_COOKIE_NAME,        # ✅ 'django_language' o'rniga settings dan
        lang,
        max_age=365 * 24 * 60 * 60,           # 1 yil
        samesite="Lax",
    )
    return response