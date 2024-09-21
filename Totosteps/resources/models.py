from django.db import models
from milestones.models import Milestone

# Create your models here.

class Resource(models.Model):
    RESOURCE_TYPES = [
        ('article', 'Article'),
        ('tutorial', 'Tutorial'),
    ]

    resource_id = models.AutoField(primary_key=True)
    milestone = models.ForeignKey(Milestone, on_delete=models.CASCADE)  # Resource tied to specific milestone
    title = models.CharField(max_length=255)
    tips = models.JSONField()
    activities = models.JSONField()
    type = models.CharField(max_length=50, choices=RESOURCE_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} {self.type}"
