from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from .models import MenuItem
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
