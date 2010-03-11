from django.conf.urls.defaults import patterns

urlpatterns = patterns('geography.views',
    (r'map/$','map'),
    (r'(?P<slug>[\w-]+)/$','location_by_name'),
)