from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from datetime import datetime


class MyUserManager(BaseUserManager):
    def create_user(self, email,password=None):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email,password=None,):
        extra_fields.setdefault('is_developer', True)
        extra_fields.setdefault('is_admin', True)
        return self.create_user(email, password)
    
    
class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(default=datetime.now)

    USER_ROLES = [
        ('Admin', 'Developer'),
        ('User', 'Parent'),
    ]
    
    user_role = models.CharField(
        max_length=50, 
        choices=USER_ROLES, 
        blank=True, 
        null=True
    ) 
    
    USERNAME_FIELD = 'email'    
    objects = MyUserManager()
    
    def __str__(self):
        return self.username
    
    



