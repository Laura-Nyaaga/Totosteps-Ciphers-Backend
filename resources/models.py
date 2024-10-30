from django.db import models
from django.core.validators import FileExtensionValidator

# Create your models here.
class Resource(models.Model):
    resource_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    tips = models.JSONField()
    activities = models.JSONField()
    image = models.ImageField(
        upload_to='resources/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"
