

from django.db import models

class Autism_Image(models.Model):
    image_id = models.PositiveSmallIntegerField(primary_key=True) 
    child_id = models.IntegerField()
    image_upload = models.ImageField(upload_to='images/')  
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)  

    def __str__(self):
        return f"{self.image_upload} {self.child_id}"
    
