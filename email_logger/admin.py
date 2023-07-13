from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.forms.widgets import Widget

# Use LongListFilterMixin if available
# (Currently internal use only)
try:
    from ixxy_admin_utils.admin_mixins import LongListFilterMixin
except ImportError:
    class LongListFilterMixin(object):
        pass

try:
    from django.utils.encoding import StrAndUnicode
except ImportError:
    from six import python_2_unicode_compatible

    @python_2_unicode_compatible
    class StrAndUnicode:
        def __str__(self):
            return self.code


try:
    from dal_admin_filters import AutocompleteFilter
except ImportError:
    AutocompleteFilter = None


from .models import EmailLog

html_script = """
<script>$(function(){
    var $frame = $('<iframe style="width:960px; height:600px;">');
    $frame.insertAfter($('#email_logger_html'));
    setTimeout(function() {
        var doc = $frame[0].contentWindow.document;
        var $body = $('body',doc);
        $body.html($('#email_logger_html').html());
        $('#email_logger_html').html('');
    }, 1 );
})
</script>
"""


class HTMLWidget(Widget):
    
    """
    Base class for all <input> widgets (except type='checkbox' and
    type='radio', which are special).
    """
    
    input_type = None  # Subclasses must define this.

    def render(self, name, value, attrs=None, renderer=None):
        if not value:
            return mark_safe('<div style="margin-left: 7em; padding-left: 30px;"></div>')
        return mark_safe('<div style="margin-left: 7em; padding-left: 30px;"><div id="email_logger_html">%s</div></div>%s' % (value, html_script))
        

class EmailLogAdminForm(forms.ModelForm):
    
    class Meta:
        model = EmailLog
        exclude = []
        widgets = {
            'html': HTMLWidget(),
        }


if AutocompleteFilter:
    
    class SubjectFilter(AutocompleteFilter):
        """
        # Add to installed apps, next to dal_select2
        'dal_admin_filters',
        
        # Update project urls.py
        from email_logger.autocomplete_views import EmailSubjectAutocomplete
        
        re_path(
            r"^email-subject-autocomplete/$",
            EmailSubjectAutocomplete.as_view(),
            name="email-subject-autocomplete",
        ),
        
        # update requrirements.txt
        dal_admin_filters==1.1.0
        
        """
        title = 'Subject'
        field_name = 'subject'
        parameter_name = 'subject'
        autocomplete_url = 'email-subject-autocomplete'
    
        def get_queryset_for_field(self, model, name):
            return EmailLog.objects.get_queryset()
    
        def get_widget(self, request):
            from dal import autocomplete
            widget = autocomplete.Select2(
                url=self.get_autocomplete_url(request),
                forward=self.get_forwards(),
            )
            return widget
else:
    SubjectFilter = 'subject'


# AutocompleteFilter
# admin.ModelAdmin
class EmailLogAdmin(admin.ModelAdmin):
    
    form = EmailLogAdminForm
    name = 'Tools and Settings'
    list_display = ('label', 'subject', 'sender', 'recipients', 'created', 'success')
    list_filter = ('label', SubjectFilter, 'sender', 'recipients', 'created', 'success')
    search_fields = ('label', 'sender', 'recipients', 'subject', 'text', 'html')
    
    def has_add_permission(self, request):
        return False

    def html(self, obj):
        return mark_safe(obj.html)
        
admin.site.register(EmailLog, EmailLogAdmin)
