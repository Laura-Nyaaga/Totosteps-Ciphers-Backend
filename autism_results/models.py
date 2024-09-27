from django.db import models

from autism_image.models import Autism_Image
from child.models import Child

class Autism_Results(models.Model):
    results_id = models.AutoField(primary_key=True)
    image = models.ForeignKey(Autism_Image, on_delete=models.CASCADE)  
    result = models.CharField(max_length=80)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
   


    def __str__(self):
        return f"Result {self.results_id} for Image {self.image.image_id}"