from django.urls import path, re_path
from . import views

urlpatterns = [
    path('payment/<int:form_entry>/<int:payment>/<int:key>/',
         views.PaymentView.as_view(), name='events.payment'),
    path('', views.DefaultView.as_view(), name='events.index'),
    ]
