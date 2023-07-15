from django.contrib import admin
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Permission

from practicetest.models import *

# Register your models here.
class PracticeTestAdmin(admin.ModelAdmin):
    fields = ['test_type','question_type','question','content','option','answer']
    list_display = ('id', 'test_type','question_type','question','option','answer','content','created_at','updated_at')
    list_per_page = 25

admin.site.register(PracticeTest, PracticeTestAdmin)

class UserPracticeAdmin(admin.ModelAdmin):
    fields = ['user','practice_test','is_challanged','is_bookmarked']
    list_display = ('id', 'user','practice_test','is_challanged','is_bookmarked','created_at','updated_at')
    list_per_page = 25

admin.site.register(UserPractice, UserPracticeAdmin)