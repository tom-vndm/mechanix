from django.db import models
from cms.models.pluginmodel import CMSPlugin

# Create your models here.


class MenuItem(CMSPlugin):
    displayName = models.CharField(max_length=128)
    pageID = models.CharField(max_length=16)

    def __str__(self):
        return self.displayName

class Masthead(CMSPlugin):
    background = models.ImageField(upload_to="Mechanix")
    alt = models.CharField(max_length=128)

    def __str__(self):
        return self.alt

class MastheadContent(CMSPlugin):
    htmlClasses = models.CharField(max_length=256)
    text = models.CharField(max_length=256)

    def __str__(self):
        return self.text

class MastheadButton(CMSPlugin):
    link = models.CharField(max_length=128)
    text = models.CharField(max_length=256)

    def __str__(self):
        return self.text