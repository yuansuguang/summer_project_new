from django.db import models

# Create your models here.

def image_path(instance, filename):
    return 'image/{0}'.format(filename)


class ImageFile(models.Model):
    image_id = models.AutoField(primary_key=True)
    instance = models.ImageField(upload_to=image_path, blank=True, default='')
