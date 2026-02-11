from django.contrib import admin
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from app.models import UserTestResult

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'phone_number')
    search_fields = ('user__username', 'email', 'phone_number')

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    extra = 0

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'is_staff', 'date_joined')
    search_fields = ('username', 'email')

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

class UserTestResultInline(admin.TabularInline):
    model = UserTestResult
    extra = 0
    readonly_fields = ('test_name', 'score', 'date_taken')

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, UserTestResultInline)

User.objects.count()
