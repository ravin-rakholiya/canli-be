from django.contrib import admin
from content.models import *

# Register your models here.
class ContentAdmin(admin.ModelAdmin):
    fields = ['uploader','type_of_content','content','extention','duration','offline_locator']
    list_display = ('id', 'uploader','type_of_content','content','extention','duration','offline_locator')
    list_per_page = 25

admin.site.register(Content, ContentAdmin)