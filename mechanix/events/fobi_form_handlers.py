import json
from django.core import mail
from fobi.base import FormHandlerPlugin, form_handler_plugin_registry, submit_plugin_form_data
from .forms import MechanixMailForm, MechanixMaxSubmissionsForm
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from fobi.models import FormEntry
from datetime import datetime
from fobi.contrib.plugins.form_handlers.db_store.models import SavedFormDataEntry

class MechanixFormMailHandlerPlugin(FormHandlerPlugin):
    """Mechanix Form Mail Handler"""

    uid = "mechanix_form_mail"
    name = "Mechanix Form Mail"
    form = MechanixMailForm

    def run(self, form_entry, request, form, form_element_entries=None):
        """To be executed by handler."""

        keys_to_avoid = [
            'paypage-orderprefix',
            'betaald',
            'eventnaam',
            'paypage-invoiceprefix'
        ]

        data = form.cleaned_data
        fields_stripped = {}
        for field in list(form_element_entries.values('plugin_data')):
            fieldContent = json.loads(field['plugin_data'])
            if (('name' in fieldContent) & ('label' in fieldContent)):
                fields_stripped[fieldContent['name']] = fieldContent['label']

        mailElements = {}

        for key in fields_stripped:
            if (key not in keys_to_avoid):
                mailElements[key] = (fields_stripped[key], data[key])

        paymentProcessed = (
            (data['paypage-orderprefix'] != '') & (data['paypage-invoiceprefix'] != ''))

        subject = 'Inschrijving/Registration ' + data['eventnaam']
        html_message = render_to_string('mail/registration.html', {
            'naam': data['voornaam'],
            'eventNaam': data['eventnaam'],
            'formData': mailElements,
            'paymentNeeded': paymentProcessed
            })
        plain_message = strip_tags(html_message)
        from_email = 'Mechanix <mechanix@vtk.be>'
        to = data['email']

        mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
    
    def plugin_data_repr(self):
        """Human readable representation of plugin data.

        :return string:
        """
        return self.data.__dict__


class MechanixMaxSubmissionsHandlerPlugin(FormHandlerPlugin):
    """Mechanix Max Submissions Handler"""

    uid = "mechanix_max_submissions"
    name = "Mechanix Max Submissions"
    form = MechanixMaxSubmissionsForm

    def run(self, form_entry, request, form, form_element_entries=None):
        """To be executed by handler."""

        max = self.data.maxSubs
        formId = form_entry.id

        submissions = SavedFormDataEntry.objects.filter(form_entry_id=formId)
        nbSubmissions = len(submissions)

        if nbSubmissions + 1 >= max:
            FormEntry.objects.filter(id=formId).update(
                active_date_to=str(datetime.now()))

    def plugin_data_repr(self):
        """Human readable representation of plugin data.

        :return string:
        """
        return self.data.__dict__


form_handler_plugin_registry.register(MechanixFormMailHandlerPlugin)
form_handler_plugin_registry.register(MechanixMaxSubmissionsHandlerPlugin)
