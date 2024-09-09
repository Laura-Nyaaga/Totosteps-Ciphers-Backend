from django.db import models

class user(models.Model):
    parent_id = models.PositiveSmallIntegerField(primary_key=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    password = models.CharField(max_length= 20)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    profile_picture = models.URLField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.phone_number}"