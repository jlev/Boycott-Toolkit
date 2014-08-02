from django.forms.widgets import Textarea
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.conf import settings

media_css = { }
media_js = (
    '%sjquery/jquery.json-2.2.min.js' % settings.STATIC_URL,
    '%sjquery/citations.js' % settings.STATIC_URL
    )

class CitationWidget(Textarea):
    def render(self, name, value, attrs=None):
        attrs['class'] = 'citable'#add citable class to div, so we can get it with jquery
        
        html = super(CitationWidget, self).render(name, value, attrs)
        html += '''Citations<div class="citation_list" id="%s"><ul></div>
        <a class="citation_link" title="Add a citation" href="#%s_citation_entry">
        <img src=%sicons/green-plus.gif>Add</a>''' % (name,name,settings.STATIC_URL)
        
        entry_div = '''<div style='display:none;' id="%s_citation_entry">
        
        <div class="fieldLabel"><label for="id_author">Author</label>:</div>
        <div class="field author_div"><input type="text" name="author" width="150" /></div>
        
        <div class="fieldLabel"><label for="id_title">Title</label>:</div>
        <div class="field title_div"><input type="text" name="title" width="150" /></div>
        
        <div class="fieldLabel"><label for="id_date">Date</label>:</div>
        <div class="field date_div"><input type="text" name="date" width="150" /></div>
        
        <div class="fieldLabel"><label for="id_url">URL</label>:</div>
        <div class="field url_div"><input type="text" name="url" width="150" /></div>
        
        <a id="%s_citation_save" class="citation_save_link" style="float:right;">&#8594; Save Citation</a>
        </div>''' % (name,name)
        js = ""
        return mark_safe("\n".join([html, entry_div, js]))
    
    class Media:
        css = media_css
        js = media_js