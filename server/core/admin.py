from django.contrib import admin
from core import models

class LanguageAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'is_archived',
    )

admin.site.register(models.Language, LanguageAdmin)