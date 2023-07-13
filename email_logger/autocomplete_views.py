from dal import autocomplete
from .models import EmailLog


class EmailSubjectAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return EmailLog.objects.none()

        qs = EmailLog.objects.all()
        if self.q:
            qs = qs.filter(subject__icontains=self.q)
            
        return qs

    def get_results(self, context):
        return [
            {
                'id': result.subject,
                'text': result.subject,
                'selected_text': self.get_selected_result_label(result),
            } for result in context['object_list']
        ]