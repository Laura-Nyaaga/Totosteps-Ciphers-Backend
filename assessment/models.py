from django.db import models

from milestones.models import Milestone

# Create your models here.

class Assessment(models.Model):
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

    QUESTION_TYPES = [
        ('multiple choice', 'Multiple Choice'),
        ('open-ended', 'Open-Ended'),
   ]
    
    question_id = models.AutoField(primary_key=True)
    milestone = models.ForeignKey(Milestone, on_delete=models.CASCADE)
    question = models.CharField(max_length=255, unique=True)
    correct_answer = models.CharField(max_length=3, choices=[('YES', 'YES'), ('NO', 'NO')])
    question_type = models.CharField(max_length=25, choices=QUESTION_TYPES)
    category = models.CharField(choices=CATEGORY_CHOICES, null=False, max_length=12)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return f"{self.question_id} {self.question}"
    
