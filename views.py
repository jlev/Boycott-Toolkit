from django.http import HttpResponse,HttpResponseNotFound
from django.template import RequestContext
from django.shortcuts import render_to_response,get_object_or_404,redirect,Http404
from django.views.decorators.cache import cache_control

from target.models import Campaign,Product
from django.contrib.auth.models import User

def deslug(name):
	bits = name.split('-')
	for i,b in enumerate(bits):
	    bits[i] = b.capitalize()
	return " ".join(bits)


@cache_control(must_revalidate=True) #so the view refreshes when we logout
def frontpage_view(request,message=None):
    if request.user.is_anonymous():
        campaigns = Campaign.objects.filter(highlight=True)
        products = Product.objects.all()[:12]
        num_users = User.objects.count()
        #if not message:
        #    message = "Welcome to the Boycott Toolkit"
        return render_to_response('frontpage_noauth.html',
            {'message':message,
            'campaigns':campaigns,'products':products},
            context_instance = RequestContext(request))
    else:
        me = request.user
        my_campaigns = me.profile.campaigns.all()
        my_products = me.profile.buy.all()
        if not message:
            message = 'Welcome back Boycotter!'
        return render_to_response('frontpage_auth.html',
            {'message':message,
            'user':me,
            'my_campaigns':my_campaigns,
            'products':my_products},
            context_instance = RequestContext(request))
        
def highlight_campaign_view(request,slug):
    name = deslug(slug)
    campaign = get_object_or_404(Campaign,name__iexact=name)
    print campaign
    if campaign.highlight:
        return redirect(campaign)
    else:
        raise Http404