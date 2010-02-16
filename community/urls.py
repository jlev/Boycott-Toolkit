from django.conf.urls.defaults import patterns

urlpatterns = patterns('community.views',
    (r'user/$','user_view_all'),
    (r'user/(?P<username>[\w-]+)/$','user_view'),
    (r'campaign/(?P<slug>[\w-]+)/$','campaign_view'),
)