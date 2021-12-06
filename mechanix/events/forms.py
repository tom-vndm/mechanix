from django import forms
from django.utils.translation import ugettext_lazy as _
from fobi.base import BasePluginForm

class MechanixMailForm(forms.Form, BasePluginForm):
    """Mail form."""
    pass


class MechanixMaxSubmissionsForm(forms.Form, BasePluginForm):
    """Max Submissions form."""

    plugin_data_fields = [
        ("maxSubs", ""),
    ]
    maxSubs = forms.IntegerField(label="Maximum submissions", required=True)


class MechanixPaymentForm(forms.Form, BasePluginForm):
    """Max Submissions form."""

    plugin_data_fields = [
        ("orderPrefix", ""),
        ("invoicePrefix", ""),
    ]
    orderPrefix = forms.IntegerField(label="Order Prefix (beheer)", required=True)
    invoicePrefix = forms.IntegerField(label="Invoice Prefix (beheer)", required=True)
