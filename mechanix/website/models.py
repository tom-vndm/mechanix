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
    subText = models.CharField(max_length=256, null=True, blank=True)
    headText = models.CharField(max_length=256, null=True, blank=True)
    buttonLink = models.CharField(max_length=512, null=True, blank=True)
    buttonText = models.CharField(max_length=256, null=True, blank=True)

    def __str__(self):
        if self.headText:
            return self.headText
        else:
            return "Masthead"


class MastheadImage(CMSPlugin):
    image = models.ImageField(upload_to="Mechanix/Masthead")
    headCaption = models.CharField(max_length=256)
    subCaption = models.CharField(max_length=256, null=True, blank=True)

    def __str__(self):
        return self.headCaption


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


class ContentFlow(CMSPlugin):
    pass

    def __str__(self):
        return "Flow"


class ContentFlowEntryImage(CMSPlugin):
    image = models.ImageField(upload_to="Mechanix/Flow")
    title = models.CharField(max_length=256, null=True, blank=True)
    subtitle = models.CharField(max_length=256, null=True, blank=True)
    content = models.CharField(max_length=2048, null=True, blank=True)

    def __str__(self):
        return self.title


class ContentFlowEntryHTML(CMSPlugin):
    text = HTMLField()

    def __str__(self):
        return "Flow HTML"


class ContentTeam(CMSPlugin):
    pass

    def __str__(self):
        return "Team"


class ContentTeamEntry(CMSPlugin):
    image = models.ImageField(upload_to="Mechanix/Team", null=True, blank=True)
    name = models.CharField(max_length=128)
    function = models.CharField(max_length=128, null=True, blank=True)
    linkedin = models.CharField(max_length=512, null=True, blank=True)
    mail = models.CharField(max_length=512, null=True, blank=True)

    def __str__(self):
        return self.name


class ContentGallery(CMSPlugin):
    pass

    def __str__(self):
        return "Team"


class ContentGalleryEntry(CMSPlugin):
    image = models.ImageField(upload_to="Mechanix/Gallery")
    alt = models.CharField(max_length=512)
    url = models.CharField(max_length=512, null=True, blank=True)

    def __str__(self):
        return self.alt


class Footer(CMSPlugin):
    pass

    def __str__(self):
        return "Footer"


class FooterTextEntry(CMSPlugin):
    text = models.CharField(max_length=512)
    url = models.CharField(max_length=512, null=True, blank=True)
    pos = models.CharField(max_length=16, choices=[(
        'L', 'Left'), ('M', 'Middle'), ('R', 'Right')])

    def __str__(self):
        return self.text


class FooterFontAwesomeEntry(CMSPlugin):
    faClass = models.CharField(max_length=512)
    url = models.CharField(max_length=512)
    pos = models.CharField(max_length=16, choices=[(
        'L', 'Left'), ('M', 'Middle'), ('R', 'Right')])

    def __str__(self):
        return self.faClass


class FooterHTMLEntry(CMSPlugin):
    text = HTMLField()
    pos = models.CharField(max_length=16, choices=[(
        'L', 'Left'), ('M', 'Middle'), ('R', 'Right')])

    def __str__(self):
        return "Footer HTML"
