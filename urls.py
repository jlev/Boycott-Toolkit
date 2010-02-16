from django.conf import settings
from django.conf.urls.defaults import *

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
    (r'^accounts/', include('registration.backends.default.urls')),
    (r'^facebook/', include('facebookconnect.urls')),
)

#my app urls
urlpatterns += patterns('boycott.views',
    (r'^$','frontpage_view'),
)
urlpatterns += patterns('',
    (r'^target/', include('target.urls')),
    (r'^community/', include('community.urls')),
)

#let django serve the static media when in debug mode
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )