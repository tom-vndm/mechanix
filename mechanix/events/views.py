from django.shortcuts import render
from django.views import View


class DefaultView(View):
    def get(self, request):
        # <view logic>
        return render(request, 'empty.html', {'teststring': 'jaja', 'page_title': 'Titel'})
