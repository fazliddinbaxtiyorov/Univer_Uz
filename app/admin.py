from django.contrib import admin
from .models import DTM_Practise, Fanlar, IELTS_Reading, IELTSListeningQuestion, Milliy_Sertifikat, IELTS_writing, SATQuestion, Davlat_Univer, Xorijiy_Univer, Xususiy_Univer, UserTestResult
# Register your models here.
from .models import ContactMessage
admin.site.register(DTM_Practise)
admin.site.register(Fanlar)
admin.site.register(IELTS_Reading)
admin.site.register(IELTSListeningQuestion)
admin.site.register(Milliy_Sertifikat)
admin.site.register(IELTS_writing)
admin.site.register(SATQuestion)
admin.site.register(Davlat_Univer)
admin.site.register(Xorijiy_Univer)
admin.site.register(Xususiy_Univer)
admin.site.register(ContactMessage)
admin.site.register(UserTestResult)