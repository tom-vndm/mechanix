from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from .models import MenuItem, Masthead, MastheadButton, MastheadContent, Content, ContentEntry, ContentHighlights, ContentHighlightsEntry
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
    render_template = "masthead/masthead.html"
    cache = False
    allow_children = True
    child_classes = ['MastheadContentPlugin', 'MastheadButtonPlugin']

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        return context


@plugin_pool.register_plugin
class MastheadContentPlugin(CMSPluginBase):
    model = MastheadContent
    name = _("Masthead content")
    render_template = "masthead/mastheadcontent.html"
    cache = False
    parent_classes = ['MastheadPlugin']

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        return context


@plugin_pool.register_plugin
class MastheadButtonPlugin(CMSPluginBase):
    model = MastheadButton
    name = _("Masthead button")
    render_template = "masthead/mastheadbutton.html"
    cache = False
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
    child_classes = ["ContentHighlightsPlugin"]
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
