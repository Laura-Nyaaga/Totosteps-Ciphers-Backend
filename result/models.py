from django.db import models
from assessment.models import Milestone
from users.models import User 

class Result(models.Model):
    id = models.AutoField(primary_key=True)
    milestone = models.ForeignKey(Milestone, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  
    answers = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"Result for {self.user.email} on {self.assessment}"