from django.conf.urls.defaults import *

urlpatterns = patterns('autocomplete.views',
    url(r'(?P<model>[\w.-]+)/objects\.json$', 'list_objects', name='autocomplete-list'),
    url(r'(?P<model>[\w.-]+)/fields\.json$', 'list_fields', name='autocomplete-fields'),
    url(r'search/','main_search_ajax',name='main_search_ajax'),
    url(r'geocode/','geocode',name='geocode')
)
