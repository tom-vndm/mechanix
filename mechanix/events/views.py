from django.shortcuts import render, HttpResponse
from django.views import View


class DefaultView(View):
    def get(self, request):
        return render(request, 'empty.html', {'teststring': 'jaja', 'page_title': 'Titel'})

class PaymentView(View):
    def get(self, request, form_entry, payment, key):
        return HttpResponse(str(form_entry) + ' ' + str(payment) + ' ' + str(key))
