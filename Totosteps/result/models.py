from django.db import models
from milestones.models import Milestone

class Result(models.Model):
    id = models.AutoField(primary_key=True)
    milestone = models.ForeignKey(Milestone, on_delete=models.CASCADE)
    answers = models.JSONField(null=True, blank=True)
    parent_email = models.EmailField()  # Add this field to store the parent's email

