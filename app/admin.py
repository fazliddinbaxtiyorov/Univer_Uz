from django.contrib import admin
from .models import DTM_Practise, Fanlar, IELTS_Reading, ReadingTest, IELTSListeningQuestion, Milliy_Sertifikat, IELTS_writing, SATQuestion, UserTestResult, ReadingTest, ListeningTest,Sat, News, DTM_Majburiy
# Register your models here.
admin.site.register(DTM_Practise)
admin.site.register(Fanlar)
admin.site.register(IELTS_Reading)
admin.site.register(IELTSListeningQuestion)
admin.site.register(Milliy_Sertifikat)
admin.site.register(IELTS_writing)
admin.site.register(SATQuestion)
admin.site.register(UserTestResult)
admin.site.register(ListeningTest)
admin.site.register(Sat)
from .models import WritingQuestion, WritingSubmission
admin.site.register(News)
admin.site.register(WritingQuestion)
admin.site.register(WritingSubmission)
@admin.register(DTM_Majburiy)
class DTMMajburiyAdmin(admin.ModelAdmin):
    list_display = ['fan', 'savol']
    list_filter = ['fan']
    search_fields = ['savol']
from django.contrib import admin
from .models import ReadingTest, IELTS_Reading


class IELTS_ReadingInline(admin.TabularInline):
    model  = IELTS_Reading
    extra  = 5
    fields = ('part', 'question_type', 'savol',
              'variant_a', 'variant_b', 'variant_c', 'variant_d',
              'togri_variant')
    ordering = ('part', 'id')


@admin.register(ReadingTest)
class ReadingTestAdmin(admin.ModelAdmin):
    inlines    = [IELTS_ReadingInline]
    list_display = ('id', 'passage_title', 'category', 'is_paid')

    fieldsets = (
        ('Part 1', {
            'fields': ('passage_title', 'passage_text'),
        }),
        ('Part 2', {
            'fields': ('passage_title_2', 'passage_text_2'),
            'classes': ('collapse',),
        }),
        ('Part 3', {
            'fields': ('passage_title_3', 'passage_text_3'),
            'classes': ('collapse',),
        }),
        ('Sozlamalar', {
            'fields': ('category', 'is_paid', 'price'),
        }),
    )
