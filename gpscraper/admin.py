from django.contrib import admin
from gpscraper.models import AppData, AppSearchIndex

class AppDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'dev_name', 'category')

admin.site.register(AppData, AppDataAdmin)
admin.site.register(AppSearchIndex)
