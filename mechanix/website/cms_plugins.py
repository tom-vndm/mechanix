from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from .models import MenuItem, Masthead, MastheadButton, MastheadContent
from .models import Content, ContentEntry, ContentHighlights, ContentHighlightsEntry
from .models import ContentGrid, ContentGridEntry, ContentFlow, ContentFlowEntryHTML
from .models import ContentFlowEntryImage, ContentTeam, ContentTeamEntry
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
    child_classes = ["ContentHighlightsPlugin",
                     'ContentGridPlugin', 'ContentFlowPlugin',
                     'ContentTeamPlugin']
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
    child_classes = ["ContentGridEntryPlugin"]
    parent_classes = ['ContentEntryPlugin']

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        return context


@plugin_pool.register_plugin
class ContentGridEntryPlugin(CMSPluginBase):
    model = ContentGridEntry
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
    render_template = "content/grid/gridmodals.html"
    cache = False

    def render(self, context, instance, placeholder):
        context['grid_modals'] = ContentGridEntry.objects.all()
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
