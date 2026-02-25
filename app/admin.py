from django.contrib import admin
from .models import DTM_Practise, Fanlar, IELTS_Reading, ReadingTest, IELTSListeningQuestion, Milliy_Sertifikat, IELTS_writing, SATQuestion, UserTestResult, ReadingTest, ListeningTest,Sat, News
# Register your models here.
admin.site.register(DTM_Practise)
admin.site.register(Fanlar)
admin.site.register(IELTS_Reading)
admin.site.register(IELTSListeningQuestion)
admin.site.register(Milliy_Sertifikat)
admin.site.register(IELTS_writing)
admin.site.register(SATQuestion)
admin.site.register(UserTestResult)
admin.site.register(ReadingTest)
admin.site.register(ListeningTest)
admin.site.register(Sat)
from .models import WritingQuestion, WritingSubmission
admin.site.register(News)
admin.site.register(WritingQuestion)
admin.site.register(WritingSubmission)

