
from django.db import models

class Child(models.Model):
    child_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField()
    profile_picture = models.ImageField(upload_to='child_profiles/', blank=True, null=True)
    is_active = models.BooleanField(default=True)  # Add this line
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} (ID: {self.child_id})"
