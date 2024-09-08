from django.db import models

class User(models.Model):
    parent_id = models.PositiveSmallIntegerField(primary_key=True, default=0)
    first_name = models.CharField(max_length=20, default='')
    last_name = models.CharField(max_length=20, default='')
    password = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20, default='')
    email = models.EmailField()
    profile_picture = models.ImageField(upload_to='profile_pictures', default='default_profile.jpg')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.phone_number}"