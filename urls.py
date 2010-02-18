from django.conf import settings
from django.conf.urls.defaults import *
from django.shortcuts import redirect

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

#admin urls
urlpatterns = patterns('',
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
)

#module urls
urlpatterns += patterns('',
    (r'^autocomplete/', include('autocomplete.urls')),
    (r'^facebook/',include('facebookconnect.urls')),    
)

#my app urls
urlpatterns += patterns('',
    (r'^target/', include('target.urls')),
    (r'^community/', include('community.urls')),
)
urlpatterns += patterns('boycott.views',
    (r'^$','frontpage_view'),
    (r'^(?P<slug>[\w-]+)/$','highlight_campaign_view'), #put this last so it can't override urls that already exist
)

#let django serve the static media when in debug mode
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )