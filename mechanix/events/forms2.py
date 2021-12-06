from django import forms
from django.utils.translation import gettext_lazy as _
from fobi.base import BaseFormFieldPluginForm, get_theme

theme = get_theme(request=None, as_instance=True)


class CounterInputForm(forms.Form, BaseFormFieldPluginForm):
    """Form for ``HiddenInputPlugin``."""

    plugin_data_fields = [
        ("label", "Counter"),
        ("name", "counter"),
        ("initial", 0)
    ]

    label = forms.CharField(
        label=_("Label"),
        required=True,
        widget=forms.widgets.TextInput(
            attrs={'class': theme.form_element_html_class}
        )
    )
    name = forms.CharField(
        label=_("Name"),
        required=True,
        widget=forms.widgets.TextInput(
            attrs={'class': theme.form_element_html_class}
        ),
        help_text=_("Don't change")
    )
    initial = forms.IntegerField(
        label=_("Initial"),
        required=True,
        widget=forms.widgets.NumberInput(
            attrs={'class': theme.form_element_html_class}
        )
    )

    def clean(self):
        super(CounterInputForm, self).clean()
