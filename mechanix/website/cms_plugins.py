from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from .models import MenuItem, Masthead, MastheadButton, MastheadContent
from django.utils.translation import gettext_lazy as _


@plugin_pool.register_plugin
class MenuItemPlugin(CMSPluginBase):
    model = MenuItem
    name = _("Menu item")
    render_template = "menu-item.html"
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
    child_classes = ['MastheadContentPlugin', 'MastheadButtonPlugin']

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        return context


@plugin_pool.register_plugin
class MastheadContentPlugin(CMSPluginBase):
    model = MastheadContent
    name = _("Masthead content")
    render_template = "mastheadcontent.html"
    cache = False
    parent_classes = ['MastheadPlugin']

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        return context


@plugin_pool.register_plugin
class MastheadButtonPlugin(CMSPluginBase):
    model = MastheadButton
    name = _("Masthead button")
    render_template = "mastheadbutton.html"
    cache = False
    parent_classes = ['MastheadPlugin']

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        return context
