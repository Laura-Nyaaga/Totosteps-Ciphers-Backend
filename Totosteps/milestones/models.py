
from django.db import models

from child.models import Child

# Create your models here.
class Milestone(models.Model):
    SOCIAL = 'Social'
    LANGUAGE = 'Language'
    COGNITIVE = 'Cognitive'
    MOVEMENT = 'Movement'

    CATEGORY_CHOICES = [
        (SOCIAL, 'Social'),
        (LANGUAGE, 'Language'),
        (COGNITIVE, 'Cognitive'),
        (MOVEMENT, 'Movement'),
    ]
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
    child_id = models.ForeignKey(Child, on_delete=models.CASCADE, null=True, blank=True)
    age = models.PositiveIntegerField(choices=AGE_IN_MONTHS)   # Age in months when this milestone applies
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    summary = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_current = models.BooleanField(default=False)

    def __str__(self):
        return f'Milestone at {self.age} months'
    
    @staticmethod
    def get_current_milestone(child_age_in_months):
        """
        Retrieving the current milestone based on the child's age.
        """
        try:
            # Get the closest milestone without exceeding the child's current age
            current_milestone = Milestone.objects.filter(age=child_age_in_months).order_by('-age').first()
            return current_milestone
        except Milestone.DoesNotExist:
            return None