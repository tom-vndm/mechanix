from django.db import models
from cms.models.pluginmodel import CMSPlugin

# Create your models here.


class MenuItem(CMSPlugin):
    displayName = models.CharField(max_length=128)
    pageID = models.CharField(max_length=16)

    def __str__(self):
        return self.displayName