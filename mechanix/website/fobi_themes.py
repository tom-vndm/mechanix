from fobi.base import theme_registry

from fobi.contrib.themes.foundation5.fobi_themes import Foundation5Theme

__all__ = ('MechanixTheme',)


class MechanixTheme(Foundation5Theme):
    html_classes = ['bg-light', ]
    base_template = 'forms/base.html'
    form_ajax = 'forms/form_ajax.html'
    base_edit_template = 'foundation5/base.html'


# It's important to set the `force` argument to True, in
# order to override the original theme. Force can be applied
# only once.
theme_registry.register(MechanixTheme, force=True)
