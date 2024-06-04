import os
from PIL import Image
from django.db import models
from django.conf import settings
from account_api.models import User
# Create your models here.

def image_directory_name(instance,filename):
    image_name = f"{instance.title}_{instance.isbn}.jpg"
    full_path = os.path.join(settings.MEDIA_ROOT, 'book_images', image_name)
    if os.path.exists(full_path):
        os.remove(full_path)
    return os.path.join(settings.MEDIA_ROOT, 'book_images', image_name)

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)
    publication_date = models.DateField(null=True, blank=True)
    publisher = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to=image_directory_name, blank=True, default='book_images/no_image.jpg')
    current_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='book_owner')
    requester = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='book_requester')
    requested = models.BooleanField(default=False)
    ongoing = models.BooleanField(default=False)

    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        SIZE = 500, 500

        if self.image:
            image = Image.open(self.image.path)
            if image.mode in ("RGBA", "p"):
                image = image.convert("RGB")
            image.thumbnail(SIZE, Image.LANCZOS)
            image.save(self.image.path)
    
    def __str__(self):
        return self.title