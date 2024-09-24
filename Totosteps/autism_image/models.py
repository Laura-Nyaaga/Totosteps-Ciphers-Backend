from django.db import models
from child.models import Child

class Autism_Image(models.Model):
    image_id = models.AutoField(primary_key=True)
    child = models.ForeignKey(Child, on_delete=models.CASCADE)  
    image_upload = models.ImageField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Image {self.image_id} for {self.child.username}"
