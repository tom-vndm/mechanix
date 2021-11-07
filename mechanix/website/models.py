from django.db import models
from cms.models.pluginmodel import CMSPlugin
from djangocms_text_ckeditor.fields import HTMLField

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


class Content(CMSPlugin):
    pass

    def __str__(self):
        return "Content"


class ContentEntry(CMSPlugin):
    htmlID = models.CharField(max_length=128)
    heading = models.CharField(max_length=256)
    subheading = models.CharField(max_length=256, null=True, blank=True)

    def __str__(self):
        return self.htmlID


class ContentHighlights(CMSPlugin):
    pass

    def __str__(self):
        return "Highlights"


class ContentHighlightsEntry(CMSPlugin):
    faIcon = models.CharField(max_length=64)
    title = models.CharField(max_length=128)
    content = models.CharField(max_length=2048)

    def __str__(self):
        return self.title


class ContentGrid(CMSPlugin):
    pass

    def __str__(self):
        return "Grid"


class ContentGridEntry(CMSPlugin):
    image = models.ImageField(upload_to="Mechanix/Grid")
    title = models.CharField(max_length=128)
    subtitle = models.CharField(max_length=128)
    description = HTMLField()
    buttonUrl = models.CharField(max_length=256, null=True, blank=True)
    buttonText = models.CharField(max_length=256, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    start = models.TimeField(null=True, blank=True)
    doors = models.TimeField(null=True, blank=True)

    def __str__(self):
        return self.title
