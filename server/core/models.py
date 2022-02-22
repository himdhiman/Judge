from pyexpat import model
from django.db import models
import uuid

class Language(models.Model):
    name = models.CharField(max_length = 20, blank = True, null = True)
    is_archived = models.BooleanField(default = False)

    def __str__(self):
        return self.name

class Submission(models.Model):
    task_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.CharField(max_length=50, blank=False)
    problem_id = models.IntegerField(blank=False)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    code = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, default="Queued")
    stderr = models.TextField(blank=True, null=True)
    test_Cases_Passed = models.IntegerField(null=True, blank=True)
    total_Test_Cases = models.IntegerField(null=True, blank=True)
    score = models.IntegerField(null=True, blank=True)
    total_score = models.IntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.task_id)