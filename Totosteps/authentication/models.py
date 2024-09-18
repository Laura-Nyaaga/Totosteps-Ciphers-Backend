import logging
from django.contrib.auth.models import AbstractUser
from django.db import models

logger = logging.getLogger(__name__)
class CustomUser(AbstractUser):
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True,
        help_text='The groups this user belongs to.'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        blank=True,
        help_text='Specific permissions for this user.'
    )

    
    def __str__(self):
       
        logger.debug('Generating string representation of user: %s', self.username)
        return self.username
    
    def save(self, *args, **kwargs):
        logger.info('Saving user instance: %s', self.username)
        super().save(*args, **kwargs)
        logger.info('User instance saved successfully: %s', self.username)
        
    class Meta:
        verbose_name = 'Custom User'
        verbose_name_plural = 'Custom Users'
