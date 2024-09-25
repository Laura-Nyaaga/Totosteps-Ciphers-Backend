from django.db import models
from django.conf import settings
from datetime import date
from dateutil.relativedelta import relativedelta

class Child(models.Model):
    child_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField()  # Use DateField instead of DateTimeField
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='children')

    def get_age_in_months(self): 
        today = date.today() 
        birth_date = self.date_of_birth  
        age = relativedelta(today, birth_date)        
        return age.years * 12 + age.months
    
    def __str__(self):
        return f"{self.username} (DOB: {self.date_of_birth})"