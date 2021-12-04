from django.db import models
from cms.models.pluginmodel import CMSPlugin
from djangocms_text_ckeditor.fields import HTMLField
from filer.fields.folder import FilerFolderField
from imagekit.models import ImageSpecField
from imagekit.processors import Adjust

# Create your models here.

class Event(models.Model):
    image = models.ImageField(upload_to="Mechanix/Event")
    image_grayscale = ImageSpecField(source='image',
                                     processors=[Adjust(color=0.0)],
                                     format='JPEG',
                                     options={'quality': 80})
    title = models.CharField(max_length=128)
    subtitle = models.CharField(max_length=128)
    description = HTMLField()
    # buttonUrl = models.CharField(max_length=256, null=True, blank=True)
    # buttonText = models.CharField(max_length=256, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    passed = models.BooleanField()
    start = models.TimeField(null=True, blank=True)
    doors = models.TimeField(null=True, blank=True)
    imageFolder = FilerFolderField(
        null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.title
