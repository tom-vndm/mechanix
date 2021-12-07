from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse
from django.views import View
from urllib.parse import urlencode
from django.utils.translation import get_language
import json, hashlib
from fobi.contrib.plugins.form_handlers.db_store.models import SavedFormDataEntry
from fobi.models import FormEntry
from .fobi_form_handlers import MechanixPaymentHandlerPlugin
from mechanix.settings import SITE_URL, EVENTS_SHA_PASS, EVENTS_PAY_URL
from django.core.exceptions import SuspiciousOperation
from django.utils.translation import gettext_lazy as _


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

        payment_data = json.loads(FormEntry.objects.filter(id=form_entry)[0] \
        .formhandlerentry_set.filter(plugin_uid=MechanixPaymentHandlerPlugin.uid)[0].plugin_data)

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

        
        hash_string, hash512 = get_hash(dict(sorted(params.items())))

        breakpoint()
        params['SHASIGN'] = str(hash512)
        return redirect(EVENTS_PAY_URL + urlencode(dict(sorted(params.items()))))


class PaidView(View):
    def get(self, request, form_entry, payment):
        return HttpResponse(str(form_entry) + ' ' + str(payment))


def get_form_data(form_entry, payment):
    form_entries = [json.loads(x['saved_data'])
                    for x in SavedFormDataEntry.objects.values() if x['form_entry_id']==form_entry]
    form_data = [x for x in form_entries if x.get('counter') == payment][0]

    form_fields = [json.loads(x['plugin_data']) for x in FormEntry.objects.filter(id=form_entry)[0].formelemententry_set.all().values()]
    choices = [x.split(', ') for x in [t['choices'] for t in form_fields if t.get('name') == 'prijs'][0].split('\r\n')]
    price = [int(x) for [x,y] in choices if y==form_data['prijs']][0]

    form_data['price_paypage']=price

    return form_data

def get_hash(params):
    hash_string = ""
    sha_in = EVENTS_SHA_PASS
    for k,v in params.items():
        hash_string += str(k) + '=' + str(v) + sha_in

    hash512 = hashlib.sha512(hash_string.encode())
    return hash_string, hash512.hexdigest()