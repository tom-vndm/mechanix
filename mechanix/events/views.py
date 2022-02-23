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
    LOGIN_URL,
)
from django.core.exceptions import SuspiciousOperation
from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core import mail
from .models import Event
import csv


class DefaultView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('%s' % (LOGIN_URL))

        header_buttons = [
            {
                'link': reverse('admin:events_event_add') + '?_popup=1',
                'text': '<i class="fas fa-plus"></i> Toevoegen',
                'popup': True,
            },
            {
                'link': reverse('fobi.dashboard'),
                'text': '<i class="fas fa-file-alt"></i> Forms Admin',
                'popup': False,
            },
        ]

        headers = [
            {
                'field_name': 'naam',
                'label': 'Naam'
            },
            {
                'field_name': 'date',
                'label': 'Datum'
            },
            {
                'field_name': 'tijd',
                'label': 'Tijd'
            },
            {
                'field_name': 'deuren',
                'label': 'Deuren'
            },
            {
                'field_name': 'subtitle',
                'label': 'Ondertitel'
            },
            {
                'field_name': 'actions',
                'label': 'Acties'
            },
        ]

        body = []
        events = Event.objects.all()
        for event in events.values():
            entries = [
                str(event['title']),
                str(event['date']),
                str(event['start']),
                str(event['doors']),
                str(event['subtitle']),
            ]

            event_id = event['id']

            buttons = [
                {
                    'link': reverse('admin:events_event_change', args=[event_id]) + '?_popup=1',
                    'text': '<i class="fas fa-edit"></i> Bewerken',
                    'popup': True,
                },
                {
                    'link': reverse('admin:events_event_delete', args=[event_id]) + '?_popup=1',
                    'text': '<i class="fas fa-trash"></i> Verwijderen',
                    'popup': True,
                },
                {
                    'link': reverse('events.forms', args=[event_id]),
                    'text': '<i class="fas fa-file-alt"></i> Forms',
                    'popup': False,
                },
            ]

            row = {
                'entries': entries,
                'buttons': buttons
            }
            body.append(row)

        return render(request, 'backend/table.html', {
            'title': 'Evenementen',
            'buttons': header_buttons,
            'headers': headers,
            'table_body': body,
        })


class EventFormsView(View):
    def get(self, request, event_id):
        if not request.user.is_authenticated:
            return redirect('%s' % (LOGIN_URL))

        header_buttons = [
            {
                'link': reverse('admin:events_event_change', args=[event_id]) + '?_popup=1',
                'text': '<i class="fas fa-edit"></i> Bewerken',
                'popup': True,
            },
            {
                'link': reverse('events.index'),
                'text': '<i class="fas fa-calendar-alt"></i> Evenementen',
                'popup': False,
            },
            {
                'link': reverse('fobi.dashboard'),
                'text': '<i class="fas fa-file-alt"></i> Forms Admin',
                'popup': False,
            },
        ]

        headers = [
            {
                'field_name': 'naam',
                'label': 'Naam'
            },
            {
                'field_name': 'public',
                'label': 'Publiek'
            },
            {
                'field_name': 'active_from',
                'label': 'Actief vanaf'
            },
            {
                'field_name': 'active_until',
                'label': 'Actief tot'
            },
            {
                'field_name': 'submissions',
                'label': 'Aantal antwoorden'
            },
            {
                'field_name': 'actions',
                'label': 'Acties'
            },
        ]

        body = []
        forms = FormEntry.objects.all()
        for form in forms.values():
            entries = [
                str(form['name']),
                str(form['is_public']),
                str(form['active_date_from']),
                str(form['active_date_to']),
            ]

            form_id = form['id']
            submissions = SavedFormDataEntry.objects.filter(
                form_entry_id=form_id)
            entries.append(str(len(submissions)))

            form_slug = form['slug']

            buttons = [
                {
                    'link': reverse('fobi.view_form_entry', args=[form_slug]),
                    'text': '<i class="fas fa-eye"></i> Openen',
                    'popup': False,
                },
                {
                    'link': reverse('fobi.edit_form_entry', args=[form_id]),
                    'text': '<i class="fas fa-edit"></i> Bewerken',
                    'popup': False,
                },
                {
                    'link': reverse('events.forms.submissions', args=[form_id]),
                    'text': '<i class="fas fa-user-friends"></i> Antwoorden',
                    'popup': False,
                },
            ]

            row = {
                'entries': entries,
                'buttons': buttons
            }
            body.append(row)

            event_name = str(Event.objects.filter(id=event_id)[0])

        return render(request, 'backend/table.html', {
            'title': event_name + ': Forms',
            'buttons': header_buttons,
            'headers': headers,
            'table_body': body,
        })


class FormSubmissionsView(View):
    def get(self, request, form_id):
        if not request.user.is_authenticated:
            return redirect('%s' % (LOGIN_URL))

        form = FormEntry.objects.filter(id=form_id).values()[0]
        form_name = form['name']
        form_fields = [json.loads(x['plugin_data']) for x in FormEntry.objects.filter(
            id=form_id)[0].formelemententry_set.all().values()]

        headers = []
        entries_to_check = []
        for field in form_fields:
            if ('label' in field) & ('name' in field):
                headers.append({
                    'field_name': field['name'],
                    'label': field['label'],
                })
                entries_to_check.append(field['name'])

        headers.append({
            'field_name': 'actions',
            'label': 'Acties'
        },)

        header_buttons = [
            {
                'link': reverse('fobi.view_form_entry', args=[form['slug']]),
                'text': '<i class="fas fa-eye"></i> Openen',
                'popup': False,
            },
            {
                'link': reverse('fobi.edit_form_entry', args=[form_id]),
                'text': '<i class="fas fa-edit"></i> Bewerken',
                'popup': False,
            },
            {
                'link': reverse('events.forms.submissions.export', args=[form_id]),
                'text': '<i class="fas fa-download"></i> Exporteren',
                'popup': False,
            },
            {
                'link': reverse('events.index'),
                'text': '<i class="fas fa-calendar-alt"></i> Evenementen',
                'popup': False,
            },
            {
                'link': reverse('fobi.dashboard'),
                'text': '<i class="fas fa-file-alt"></i> Forms Admin',
                'popup': False,
            },
        ] 

        body = []
        form_entries = [json.loads(x['saved_data'])
                        for x in SavedFormDataEntry.objects.values() if x['form_entry_id'] == form_id]
        for entry in form_entries:
            entries = []
            for check in entries_to_check:
                entries.append(entry.get(check, 'None'))
            buttons = [
                {
                    'link': reverse('events.forms.submission.edit', args=[form_id,int(entry.get('counter'))]),
                    'text': '<i class="fas fa-edit"></i> Bewerken',
                    'popup': False,
                },
                {
                    'link': reverse('events.forms.submission.delete', args=[form_id, int(entry.get('counter'))]),
                    'text': '<i class="fas fa-trash"></i> Verwijderen',
                    'popup': False,
                },
            ]

            row = {
                'entries': entries,
                'buttons': buttons
            }
            body.append(row)

        return render(request, 'backend/table.html', {
            'title': form_name + ': Antwoorden',
            'buttons': header_buttons,
            'headers': headers,
            'table_body': body,
        })


class FormSubmissionEditView(View):
    def get(self, request, form_id, entry_id):
        if not request.user.is_authenticated:
            return redirect('%s' % (LOGIN_URL))
        header_buttons = [
            {
                'link': reverse('events.index'),
                'text': '<i class="fas fa-calendar-alt"></i> Evenementen',
                'popup': False,
            },
            {
                'link': reverse('events.forms.submissions', args=[form_id]),
                'text': '<i class="fas fa-user-friends"></i> Antwoorden',
                'popup': False,
            },
            {
                'link': reverse('fobi.dashboard'),
                'text': '<i class="fas fa-file-alt"></i> Forms Admin',
                'popup': False,
            },
        ]

        form_values = SavedFormDataEntry.objects.filter(form_entry_id=form_id)
        form_names = json.loads(form_values.values()[0]['form_data_headers'])
        form_submission = [x['saved_data'] for x in form_values.values() if json.loads(x['saved_data']).get('counter') == entry_id][0]
        form_submission_dict = json.loads(form_submission)
        # form_fields = [json.loads(x['plugin_data']) for x in FormEntry.objects.filter(id=form_id)[0].formelemententry_set.all().values()]

        form = []
        for k, v in form_submission_dict.items():
            disabled = (k in [
                'counter',
                'privacy',
                'privacy2',
                'privacy3',
            ])
            form.append({
                'name': k,
                'label': form_names[k],
                'type': 'text',
                'content': v,
                'disabled': disabled
            })

        return render(request, 'backend/form.html', {
            'title': 'Antwoord bewerken: ' + str(entry_id),
            'buttons': header_buttons,
            'form': form,
        })

    def post(self, request, form_id, entry_id):
        if not request.user.is_authenticated:
            return redirect('%s' % (LOGIN_URL))

        post = request.POST.dict()
        post.pop('csrfmiddlewaretoken')
        
        form_values = SavedFormDataEntry.objects.filter(form_entry_id=form_id)
        form_submission = [x['saved_data'] for x in form_values.values(
        ) if json.loads(x['saved_data']).get('counter') == entry_id][0]

        for k, v in json.loads(form_submission).items():
            if type(v) is int:
                post[k] = int(post[k])
            if type(v) is bool:
                post[k] = bool(post[k])

        form_submission_update = json.dumps(post)

        form_submission_select = SavedFormDataEntry.objects.filter(
            saved_data=form_submission)
        form_submission_select.update(saved_data=form_submission_update)

        return redirect(reverse('events.forms.submissions', args=[form_id]))


class FormSubmissionDeleteView(View):
    def get(self, request, form_id, entry_id):
        if not request.user.is_authenticated:
            return redirect('%s' % (LOGIN_URL))

        id = [x['id'] for x in SavedFormDataEntry.objects.filter(form_entry_id=form_id).values() if json.loads(x['saved_data'])['counter'] == entry_id][0]
        SavedFormDataEntry.objects.get(id=id).delete()
        return redirect(reverse('events.forms.submissions', args=[form_id]))


class FormSubmissionsExportView(View):
    def get(self, request, form_id):
        if not request.user.is_authenticated:
            return redirect('%s' % (LOGIN_URL))
        response = HttpResponse(
            content_type='text/csv',
            headers={
                'Content-Disposition': 'attachment; filename="export.csv"'},
        )

        writer = csv.writer(response)

        form = FormEntry.objects.filter(id=form_id).values()[0]
        form_fields = [json.loads(x['plugin_data']) for x in FormEntry.objects.filter(
            id=form_id)[0].formelemententry_set.all().values()]

        headers = []
        entries_to_check = []
        for field in form_fields:
            if ('label' in field) & ('name' in field):
                headers.append(field['name'])
                entries_to_check.append(field['name'])

        writer.writerow(headers)

        form_entries = [json.loads(x['saved_data'])
                        for x in SavedFormDataEntry.objects.values() if x['form_entry_id'] == form_id]
        for entry in form_entries:
            entries = []
            for check in entries_to_check:
                entries.append(entry.get(check, 'None'))
            writer.writerow(entries)

        return response
        

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
            'HOMEURL': 'http://mechanix.vtk.be',
        }

        hash512 = get_hash(dict(sorted(params.items())), EVENTS_SHA_PASS)
        params['SHASIGN'] = str(hash512)

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
            'orderID',
            'PAYID',
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

        if orderid != data['orderID']:
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
    for k, v in sorted(params.items(), key=lambda kv: str(kv[0])):
        hash_string += str(k).upper() + '=' + str(v).upper() + sha_in

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
        _('CN'): form_data.get('voornaam') + ' ' + form_data.get('achternaam'),
        _('optie'): form_data.get('prijs'),
        _('ORDERID'): data.get('orderID'),
        _('ticket_nummer'): form_data.get('counter'),
        _('payid'): data.get('PAYID'),
    }
    
    subject = _('payment-received') + ' ' + form_data.get('eventnaam')
    html_message = render_to_string('mail/payment.html', {
        'naam': form_data.get('voornaam'),
        'eventNaam': form_data.get('eventnaam'),
        'formData': mailElements,
    })
    plain_message = strip_tags(html_message)
    from_email = 'Mechanix <mechanix@vtk.be>'
    to = form_data.get('email')

    mail.send_mail(subject, plain_message, from_email,
                   [to], html_message=html_message)
