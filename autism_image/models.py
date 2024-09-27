from django.db import models
from django.core.exceptions import ValidationError
from child.models import Child
from django.utils.translation import gettext_lazy as _
from django.core.files.uploadedfile import UploadedFile

class Autism_Image(models.Model):
    image_id = models.AutoField(primary_key=True)
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    image_upload = models.ImageField(upload_to='autism_detector/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if not self.image_upload: 
            raise ValidationError(_("Image file is required."))

        if hasattr(self.image_upload, 'file') and isinstance(self.image_upload.file, UploadedFile): 
            file_type = self.image_upload.file.content_type
            if file_type not in ['image/jpeg', 'image/png']:
                raise ValidationError(_('Unsupported file type. Only JPEG and PNG images are allowed.'))

    def save(self, *args, **kwargs):
        self.full_clean() 
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Image {self.image_id} for {self.child.username}"

