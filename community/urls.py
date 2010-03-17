from django.conf.urls.defaults import *

urlpatterns = patterns('community.views',
    url(r'^login/$','login_view',name='auth_login'), #so facebookconnect can find the right view
    url(r'^logout/$','logout_view',name='auth_logout'),
    url(r'^change_password/$','change_password_view',name='auth_password_change'),
    url(r'^register/$','register_view'),
    url(r'^user/$','user_view_all'),
    url(r'^user/(?P<username>[\w-]+)/$','user_view'),
    url(r'^user/(?P<username>[\w-]+)/edit/$','user_edit'),
)