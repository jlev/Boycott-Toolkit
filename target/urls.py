from django.conf.urls.defaults import patterns

urlpatterns = patterns('target.views',
    (r'company/$','company_view_all'),
    (r'company/new/$','company_add'),
    (r'company/(?P<slug>[\w-]+)/$','company_view'),
    (r'company/(?P<slug>[\w-]+)/edit/$','company_edit'),
    (r'product/$','product_view_all'),
    (r'product/new/$','product_add'),
    (r'product/(?P<slug>[\w-]+)/$','product_view'),
    (r'product/(?P<slug>[\w-]+)/edit/$','product_edit'),
    (r'tag/(?P<tag>[\w-]+)/$','tag_view'),
    (r'campaign/$','campaign_view_all'),
    (r'campaign/new/$','campaign_add'),
    (r'campaign/(?P<slug>[\w-]+)/$','campaign_view'),
    (r'campaign/(?P<slug>[\w-]+)/edit/$','campaign_edit'),
)