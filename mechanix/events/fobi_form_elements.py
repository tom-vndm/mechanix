from django.forms.fields import IntegerField
from django.forms.widgets import HiddenInput
from django.utils.translation import gettext_lazy as _
from fobi.base import FormFieldPlugin, get_theme, form_element_plugin_registry
from .forms2 import CounterInputForm
from fobi.contrib.plugins.form_handlers.db_store.models import SavedFormDataEntry

theme = get_theme(request=None, as_instance=True)


class CounterInputPlugin(FormFieldPlugin):
    """Hidden field plugin."""

    uid = 'counter'
    name = _("Counter")
    group = _("Fields")
    form = CounterInputForm
    is_hidden = True

    def get_form_field_instances(self, request=None, form_entry=None,
                                 form_element_entries=None, **kwargs):
        """Get form field instances."""
        field_kwargs = {
            'label': self.data.label,
            'initial': self.data.initial,
            'widget': HiddenInput(
                attrs={'class': theme.form_element_html_class}
            ),
        }

        return [(self.data.name, IntegerField, field_kwargs)]
        # return [(self.data.name, (CharField, TextInput), kwargs)]

    def submit_plugin_form_data(self, form_entry, request, form, form_element_entries=None, **kwargs):
        """Submit plugin form data."""
        breakpoint()

        formId = form_entry.id
        submissions = SavedFormDataEntry.objects.filter(form_entry_id=formId)
        nbSubmissions = len(submissions)

        form.cleaned_data[self.data.name] = self.data.initial + nbSubmissions + 1
        
        return form


form_element_plugin_registry.register(CounterInputPlugin)