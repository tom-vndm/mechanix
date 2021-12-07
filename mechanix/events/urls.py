from django.urls import path, re_path
from . import views

urlpatterns = [
     path('payment/<int:form_entry>/<int:payment>/<int:key>/',
          views.PaymentView.as_view(), name='events.payment'),
     path('paid/<int:form_entry>/<int:payment>/',
          views.PaidView.as_view(), name='events.paid'),
     path('event/<int:event_id>',
          views.EventFormsView.as_view(), name='events.forms'),
    path('event/submissions/<int:form_id>/export',
         views.FormSubmissionsExportView.as_view(), name='events.forms.submissions.export'),
    path('event/submissions/<int:form_id>/<int:entry_id>/edit',
         views.FormSubmissionEditView.as_view(), name='events.forms.submission.edit'),
    path('event/submissions/<int:form_id>/<int:entry_id>/delete',
         views.FormSubmissionDeleteView.as_view(), name='events.forms.submission.delete'),
    path('event/submissions/<int:form_id>',
         views.FormSubmissionsView.as_view(), name='events.forms.submissions'),
     path('', 
          views.DefaultView.as_view(), name='events.index'),
]
