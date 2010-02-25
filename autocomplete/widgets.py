from django.forms.widgets import Input
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

js_base_url = getattr(settings, 'AUTOCOMPLETE_JS_BASE_URL','%sautocomplete/' % settings.MEDIA_URL)
media_css = {
    'all': ('%sjquery.autocomplete.css' % js_base_url,)
}
media_js = (
    'http://ajax.googleapis.com/ajax/libs/jquery/1.4/jquery.min.js',
    '%sjquery.autocomplete.js' % js_base_url,
    )

class TagAutocomplete(Input):
    '''Autocompletes for tags'''
    input_type = 'text'
    
    def render(self, name, value, attrs=None):
        ajax_url = reverse('autocomplete-list',kwargs={'model':'tagging.tag'})
        html = super(TagAutocomplete, self).render(name, value, attrs)
        js = u'''<script type="text/javascript">
            $().ready(function() { $("#%s").autocomplete("%s", { multiple: true }); });
            </script>''' % (attrs['id'],ajax_url)
        return mark_safe("\n".join([html, js]))
    
    class Media:
        css = media_css
        js = media_js

class Autocomplete(Input):
    '''Autocompletes the objects of a model passed in attrs'''
    input_type = 'text'
    
    def render(self, name, value, attrs=None):
        #retrieve the model name from attrs, popping so isn't passed to super
        ajax_url = reverse('autocomplete-list',kwargs={'model':self.attrs.pop('model')})
        html = super(Autocomplete, self).render(name, value, attrs)
        js = u'''<script type="text/javascript">
            $().ready(function() { $("#%s").autocomplete("%s", { multiple: true }); });
            </script>''' % (attrs['id'],ajax_url)
        return mark_safe("\n".join([html, js]))
    
    class Media:
        css = media_css
        js = media_js

class DynamicAutocomplete(Input):
    '''Autocompletes based on the value of another field'''
    input_type = 'text'

    def render(self, name, value, attrs=None):
        html = super(DynamicAutocomplete, self).render(name, value, attrs)
        attrs['search_name'] = self.attrs['search_name'] #copy to local
        js = u'''<script type="text/javascript">
            $().ready(function() {
                search_value = jQuery("#%(search_name)s").value();
                $("#%(id)s").attr('callback_url',"/autocomplete/"+search_value+"/objects.json");
                    //FINISH: set the callback url to the value of the search_name field
                $("#%(id)s").autocomplete($("#%(id)s").attr('callback_url'), { multiple: true });
            });
            </script>''' % attrs
        return mark_safe("\n".join([html, js]))

    class Media:
        css = media_css
        js = media_js