from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, role=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        
        if not role:
            raise ValueError('The Role field must be set')  # Ensure role is provided
        
        email = self.normalize_email(email)
        user = self.model(email=email, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')  # Default role for superuser is 'admin'
        
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    # Role choices
    ADMIN = 'admin'
    PARENT = 'parent'
    
    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (PARENT, 'Parent'),
    ]
    
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='parent') 
    is_staff = models.BooleanField(default=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['role']  
    
    def __str__(self):
        return f"{self.email}"

    def clean(self):
        # Ensure only superusers have the admin role
        if self.role == 'admin' and not self.is_superuser:
            raise ValidationError(_('Admin role can only be assigned to superusers.'))

        if self.is_superuser and self.role != 'admin':
            raise ValidationError(_('Superusers must have the admin role.'))

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_parent(self):
        return self.role == self.PARENT
    
