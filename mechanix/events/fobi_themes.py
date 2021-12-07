from fobi.base import theme_registry

from fobi.contrib.themes.foundation5.fobi_themes import Foundation5Theme

__all__ = ('MechanixTheme',)


class MechanixTheme(Foundation5Theme):
    html_classes = ['bg-light', ]
    base_template = 'forms/base.html'
    form_ajax = 'forms/form_ajax.html'
    base_edit_template = 'forms/base_old.html'
    messages_snippet_template_name = 'forms/messages_snippet.html'
    form_entry_inactive_ajax_template = 'forms/form_entry_inactive_ajax.html'
    form_entry_submitted_ajax_template = 'forms/form_entry_submitted_ajax.html'


# It's important to set the `force` argument to True, in
# order to override the original theme. Force can be applied
# only once.
theme_registry.register(MechanixTheme, force=True)
