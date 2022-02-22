from django.contrib import admin
from core import models

class LanguageAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'is_archived',
    )

class submissionAdmin(admin.ModelAdmin):
    list_display = (
        "created_by",
        "language",
        "status",
        "timestamp",
    )


admin.site.register(models.Language, LanguageAdmin)
admin.site.register(models.Submission, submissionAdmin)