from django.conf.urls.defaults import *

urlpatterns = patterns('info.views',
    (r'^(?P<id>[\d-]+)/$','source_view'),
)