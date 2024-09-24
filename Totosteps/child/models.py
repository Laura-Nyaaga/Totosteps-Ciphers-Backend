from django.db import models
from django.conf import settings
class Child(models.Model):
    child_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='children')

    def __str__(self):
        return f"{self.username} (DOB: {self.date_of_birth})"