from django.db import models

from autism_image.models import Autism_Image
from django.utils.timezone import now

class Autism_Results(models.Model):
    results_id = models.IntegerField()
    image_id = models.ForeignKey(Autism_Image, on_delete=models.CASCADE)
    result = models.CharField(max_length=80)
    updated_at = models.DateTimeField(default=now)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.result}"