from django.contrib import admin
from .models import Students, DTM_Practise, Fanlar, IELTS_Reading, IELTS_listening
# Register your models here.
admin.site.register(Students)
admin.site.register(DTM_Practise)
admin.site.register(Fanlar)
admin.site.register(IELTS_Reading)
admin.site.register(IELTS_listening)
