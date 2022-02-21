from django.db import models

class Language(models.Model):
    name = models.CharField(max_length = 20, blank = True, null = True)
    is_archived = models.BooleanField(default = False)

    def __str__(self):
        return self.name