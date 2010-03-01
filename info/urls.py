from django.conf.urls.defaults import patterns

urlpatterns = patterns('info.views',
    (r'(?P<id>[\d-]+)$','source_view'),
)