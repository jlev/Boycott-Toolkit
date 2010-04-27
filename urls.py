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
    (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': settings.MEDIA_URL + '/logo/favicon.ico'}),
	(r'^robots\.txt$','django.views.generic.simple.redirect_to', {'url': settings.MEDIA_URL + 'robots.txt'}),
)

#module urls
urlpatterns += patterns('',
    (r'^autocomplete/', include('autocomplete.urls')),
    (r'^facebook/',include('facebookconnect.urls')),    
    (r'^comments/', include('django.contrib.comments.urls')), 
)

#my app urls
urlpatterns += patterns('',
    (r'^target/', include('target.urls')),
    (r'^community/', include('community.urls')),
    (r'^location/', include('geography.urls')),
    (r'proxy/(?P<theURL>.*)$','boycott.views.proxy'),
    (r'^source/', include('info.urls')),
)
urlpatterns += patterns('boycott.views',
    (r'^$','frontpage_view'),
    (r'^search/$','search_view'), #query sent in request
    #put this last so it can't override urls that already exist
    (r'^(?P<slug>[\w-]+)/$','highlight_campaign_view'),
)

#let django serve the static media when in debug mode
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )