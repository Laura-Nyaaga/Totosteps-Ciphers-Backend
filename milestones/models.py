from django.db import models
from django.core.validators import FileExtensionValidator

# Create your models here.
class Milestone(models.Model):
    AGE_IN_MONTHS=[
        (2, '2 Months'),
        (4, '4 Months'),
        (6, '6 Months'),
        (9, '9 Months'),
        (12, '12 Months'),
        (15, '15 Months'),
        (18, '18 Months'),
        (24, '24 Months'),
        (30, '30 Months'),
        (36, '36 Months'),
    ]

    milestone_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    age = models.PositiveIntegerField(choices=AGE_IN_MONTHS)   
    description = models.TextField()
    summary = models.JSONField()
    image = models.ImageField(
        upload_to='milestones/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'{self.name} at {self.age} months'