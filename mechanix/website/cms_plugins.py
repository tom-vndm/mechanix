from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from .models import MenuItem, Masthead, MastheadImage
from .models import Content, ContentEntry, ContentHighlights, ContentHighlightsEntry
from .models import ContentGrid, Event, ContentFlow, ContentFlowEntryHTML
from .models import ContentFlowEntryImage, ContentTeam, ContentTeamEntry
from .models import ContentGallery, ContentGalleryEntry, Footer, FooterTextEntry
from .models import FooterFontAwesomeEntry, FooterHTMLEntry
from django.utils.translation import gettext_lazy as _


@plugin_pool.register_plugin
class MenuItemPlugin(CMSPluginBase):
    model = MenuItem
    name = _("Menu item")
    render_template = "menuitem.html"
    cache = False

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        return context


@plugin_pool.register_plugin
class MastheadPlugin(CMSPluginBase):
    model = Masthead
    name = _("Masthead")
    render_template = "masthead.html"
    cache = False
    allow_children = True
    child_classes = ['MastheadImagePlugin']

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        return context


@plugin_pool.register_plugin
class MastheadImagePlugin(CMSPluginBase):
    model = MastheadImage
    name = _("Masthead Image")
    cache = False
    render_plugin = False
    parent_classes = ['MastheadPlugin']

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        return context


@plugin_pool.register_plugin
class ContentPlugin(CMSPluginBase):
    model = Content
    name = _("Content wrapper")
    render_template = "content/content.html"
    cache = False
    allow_children = True
    child_classes = ['ContentEntryPlugin']

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        return context


@plugin_pool.register_plugin
class ContentEntryPlugin(CMSPluginBase):
    model = ContentEntry
    name = _("Content entry")
    render_template = "content/contententry.html"
    cache = False
    allow_children = True
    child_classes = ["ContentHighlightsPlugin",
                     'ContentGridPlugin', 'ContentFlowPlugin',
                     'ContentTeamPlugin', 'ContentGalleryPlugin']
    parent_classes = ['ContentPlugin']

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        return context


@plugin_pool.register_plugin
class ContentHighlightsPlugin(CMSPluginBase):
    model = ContentHighlights
    name = _("Highlights")
    render_template = "content/highlights/highlights.html"
    cache = False
    allow_children = True
    child_classes = ["ContentHighlightsEntryPlugin"]
    parent_classes = ['ContentEntryPlugin']

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        return context


@plugin_pool.register_plugin
class ContentHighlightsEntryPlugin(CMSPluginBase):
    model = ContentHighlightsEntry
    name = _("Highlights entry")
    render_template = "content/highlights/highlightsentry.html"
    cache = False
    parent_classes = ['ContentHighlightsPlugin']

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        return context


@plugin_pool.register_plugin
class ContentGridPlugin(CMSPluginBase):
    model = ContentGrid
    name = _("Grid")
    render_template = "content/grid/grid.html"
    cache = False
    allow_children = True
    child_classes = ["EventPlugin"]
    parent_classes = ['ContentEntryPlugin']

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        return context


@plugin_pool.register_plugin
class EventPlugin(CMSPluginBase):
    model = Event
    name = _("Grid entry")
    render_template = "content/grid/gridentry.html"
    cache = False
    parent_classes = ['ContentGridPlugin']

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        return context


@plugin_pool.register_plugin
class ContentModalPlugin(CMSPluginBase):
    name = _("Modals")
    render_template = "content/modals.html"
    cache = False

    def render(self, context, instance, placeholder):
        context['grid_modals'] = Event.objects.all()
        context['team_modals'] = ContentTeamEntry.objects.all()
        context = super().render(context, instance, placeholder)
        return context


@plugin_pool.register_plugin
class ContentFlowPlugin(CMSPluginBase):
    model = ContentFlow
    name = _("Flow")
    render_template = "content/flow/flow.html"
    cache = False
    allow_children = True
    child_classes = ["ContentFlowEntryImagePlugin",
                     "ContentFlowEntryHTMLPlugin"]
    parent_classes = ['ContentEntryPlugin']

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        return context


@plugin_pool.register_plugin
class ContentFlowEntryImagePlugin(CMSPluginBase):
    model = ContentFlowEntryImage
    name = _("Flow entry (image)")
    render_template = "content/flow/flowentry-image.html"
    cache = False
    parent_classes = ['ContentFlowPlugin']

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        return context


@plugin_pool.register_plugin
class ContentFlowEntryHTMLPlugin(CMSPluginBase):
    model = ContentFlowEntryHTML
    name = _("Flow entry (html)")
    render_template = "content/flow/flowentry-text.html"
    cache = False
    parent_classes = ['ContentFlowPlugin']

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        return context


@plugin_pool.register_plugin
class ContentTeamPlugin(CMSPluginBase):
    model = ContentTeam
    name = _("Team")
    render_template = "content/team/team.html"
    cache = False
    allow_children = True
    child_classes = ["ContentTeamEntryPlugin"]
    parent_classes = ['ContentEntryPlugin']

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        return context


@plugin_pool.register_plugin
class ContentTeamEntryPlugin(CMSPluginBase):
    model = ContentTeamEntry
    name = _("Team entry")
    render_template = "content/team/teamentry.html"
    cache = False
    parent_classes = ['ContentTeamPlugin']

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        return context


@plugin_pool.register_plugin
class ContentGalleryPlugin(CMSPluginBase):
    model = ContentGallery
    name = _("Gallery")
    render_template = "content/gallery/gallery.html"
    cache = False
    allow_children = True
    child_classes = ["ContentGalleryEntryPlugin"]
    parent_classes = ['ContentEntryPlugin']

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        return context


@plugin_pool.register_plugin
class ContentGalleryEntryPlugin(CMSPluginBase):
    model = ContentGalleryEntry
    name = _("Gallery entry")
    render_template = "content/gallery/galleryentry.html"
    cache = False
    parent_classes = ['ContentGalleryPlugin']

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        return context


@plugin_pool.register_plugin
class FooterPlugin(CMSPluginBase):
    model = Footer
    name = _("Footer")
    render_template = "footer/footer.html"
    cache = False
    allow_children = True
    child_classes = ["FooterTextEntryPlugin",
                     "FooterFontAwesomeEntryPlugin", "FooterHTMLEntryPlugin"]

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        return context


@plugin_pool.register_plugin
class FooterTextEntryPlugin(CMSPluginBase):
    model = FooterTextEntry
    name = _("Footer text entry")
    render_template = "footer/footertextentry.html"
    cache = False
    parent_classes = ['FooterPlugin']

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        return context


@plugin_pool.register_plugin
class FooterFontAwesomeEntryPlugin(CMSPluginBase):
    model = FooterFontAwesomeEntry
    name = _("Footer FontAwesome entry")
    render_template = "footer/footerFAentry.html"
    cache = False
    parent_classes = ['FooterPlugin']

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        return context


@plugin_pool.register_plugin
class FooterHTMLEntryPlugin(CMSPluginBase):
    model = FooterHTMLEntry
    name = _("Footer html entry")
    render_template = "footer/footerhtmlentry.html"
    cache = False
    parent_classes = ['FooterPlugin']

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        return context
