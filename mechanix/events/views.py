from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse
from django.views import View
from urllib.parse import urlencode
from django.utils.translation import get_language
import json
import hashlib
from fobi.contrib.plugins.form_handlers.db_store.models import SavedFormDataEntry
from fobi.models import FormEntry
from .fobi_form_handlers import MechanixPaymentHandlerPlugin
from mechanix.settings import (
    SITE_URL, 
    EVENTS_SHA_PASS, 
    EVENTS_PAY_URL,
    EVENTS_SHA_OUT,
)
from django.core.exceptions import SuspiciousOperation
from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core import mail


class DefaultView(View):
    def get(self, request):
        return render(request, 'empty.html', {'teststring': 'jaja', 'page_title': 'Titel'})


class PaymentView(View):
    def get(self, request, form_entry, payment, key):

        form_data = get_form_data(form_entry, payment)

        if key != form_data['random']:
            raise SuspiciousOperation(_("random_key_incorrect"))

        invoice_nb_int = form_data['counter']
        invoice_nb = str(invoice_nb_int).zfill(4)

        payment_data = get_payment_data(form_entry)

        session_lang = get_language()
        lang_mapper = {
            'nl': 'nl_NL',
            'en': 'en_US',
        }
        paypage_lang = lang_mapper.get(session_lang, 'en_US')
        params = {
            'COM': str(payment_data['invoicePrefix']) + invoice_nb,
            'ORDERID': str(payment_data['orderPrefix']) + invoice_nb,
            'ACCEPTURL': SITE_URL + reverse('events.paid', kwargs={'form_entry': form_entry, 'payment': invoice_nb_int}),
            'AMOUNT': form_data['price_paypage'],
            'CN': form_data['voornaam'] + ' ' + form_data['achternaam'],
            'CURRENCY': 'EUR',
            'EMAIL': form_data['email'],
            'LANGUAGE': paypage_lang,
            'LOGO': 'logo.png',
            'PMLISTTYPE': '2',
            'PSPID': 'vtkprod',
            'TP': 'ingenicoResponsivePaymentPageTemplate_index.html',
        }

        hash512 = get_hash(dict(sorted(params.items())), EVENTS_SHA_PASS)
        params['SHASIGN'] = str(hash512)

        breakpoint()
        url = EVENTS_PAY_URL + urlencode(dict(sorted(params.items())))
        return redirect(url)


class PaidView(View):
    def get(self, request, form_entry, payment):
        data_raw = dict(request.GET)

        data = {}
        for k, v in data_raw.items():
            data[k] = v[0]

        if not all (k in data.keys() for k in (
            'SHASIGN',
            'COM',
            'ORDERID',
        )):
            raise SuspiciousOperation(_("incomplete_request"))

        sha_out = str(data.pop('SHASIGN'))
        sha_out_true = get_hash(data, EVENTS_SHA_OUT)

        if sha_out.capitalize() != sha_out_true.capitalize():
            raise SuspiciousOperation(_("sha_out_incorrect"))

        form_data = get_form_data(form_entry, payment)
        payment_data = get_payment_data(form_entry)

        invoice_nb_int = form_data['counter']
        invoice_nb = str(invoice_nb_int).zfill(4)

        com = str(payment_data['invoicePrefix']) + invoice_nb
        orderid = str(payment_data['orderPrefix']) + invoice_nb

        if (com, orderid) != (data['COM'], data['ORDERID']):
            raise SuspiciousOperation(_("order_incorrect"))

        set_paid(form_entry, payment)
        send_confirmation(data, form_data)

        form_entry_slug = FormEntry.objects.filter(id=form_entry).values()[0]['slug']

        confirmation_page = reverse(
            'fobi.form_entry_submitted', args=[form_entry_slug])
        return redirect(confirmation_page)


def get_form_data(form_entry, payment):
    form_entries = [json.loads(x['saved_data'])
                    for x in SavedFormDataEntry.objects.values() if x['form_entry_id'] == form_entry]
    form_data = [x for x in form_entries if x.get('counter') == payment][0]

    form_fields = [json.loads(x['plugin_data']) for x in FormEntry.objects.filter(
        id=form_entry)[0].formelemententry_set.all().values()]
    choices = [x.split(', ') for x in [t['choices']
                                       for t in form_fields if t.get('name') == 'prijs'][0].split('\r\n')]
    price = [int(x) for [x, y] in choices if y == form_data['prijs']][0]

    form_data['price_paypage'] = price

    return form_data


def get_hash(params, sha_in):
    hash_string = ""
    for k, v in params.items():
        hash_string += str(k) + '=' + str(v) + sha_in

    hash512 = hashlib.sha512(hash_string.encode())
    return hash512.hexdigest()


def get_payment_data(form_entry):
    return json.loads(FormEntry.objects.filter(id=form_entry)[0]
                      .formhandlerentry_set.filter(plugin_uid=MechanixPaymentHandlerPlugin.uid)[0].plugin_data)


def set_paid(form_entry, payment):
    form_values = SavedFormDataEntry.objects.filter(form_entry_id=form_entry)
    form_submission = [x['saved_data']
                       for x in form_values.values() if json.loads(x['saved_data']).get('counter') == payment][0]
    form_submission_dict = json.loads(form_submission)

    form_submission_dict['betaald'] = 'Ja'
    form_submission_paid = json.dumps(form_submission_dict)

    form_submission_select = SavedFormDataEntry.objects.filter(saved_data=form_submission)
    form_submission_select.update(saved_data=form_submission_paid)


def send_confirmation(data, form_data):
    mailElements = {
        _('CN'): data.get('CN'),
        _('optie'): form_data.get('prijs'),
        _('valuta'): data.get('CURRENCY'),
        _('amount'): data.get('AMOUNT'),
        _('ORDERID'): data.get('ORDERID'),
        _('ticket_nummer'): form_data['counter']
    }
    breakpoint()

    subject = _('payment-received') + ' ' + form_data['eventnaam']
    html_message = render_to_string('mail/payment.html', {
        'naam': form_data['voornaam'],
        'eventNaam': form_data['eventnaam'],
        'formData': mailElements,
    })
    plain_message = strip_tags(html_message)
    from_email = 'Mechanix <mechanix@vtk.be>'
    to = form_data['email']

    mail.send_mail(subject, plain_message, from_email,
                   [to], html_message=html_message)
