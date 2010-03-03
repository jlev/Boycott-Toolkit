from django.http import HttpResponse,HttpResponseNotFound
from django.template import RequestContext
from django.shortcuts import render_to_response,get_object_or_404,redirect,Http404
from django.views.decorators.cache import cache_control

from django.contrib.auth.models import User
from target.models import Campaign,Product,Company
from geography.models import Location

def deslug(name):
	bits = name.split('-')
	for i,b in enumerate(bits):
	    bits[i] = b.capitalize()
	return " ".join(bits)


@cache_control(must_revalidate=True) #so the view refreshes when we logout
def frontpage_view(request,message=None):
    if request.user.is_anonymous():
        campaigns = Campaign.objects.filter(highlight=True)
        num_campaigns = Campaign.objects.count()
        products = Product.objects.all()[:12]
        num_users = User.objects.count()
        #if not message:
        #    message = "Welcome to the Boycott Toolkit"
        return render_to_response('frontpage_noauth.html',
            {'message':message,
            'campaigns':campaigns,
            'num_campaigns':num_campaigns,
            'products':products},
            context_instance = RequestContext(request))
    else:
        my_profile = request.user.profile
        my_campaigns = my_profile.campaigns.all()
        my_companies_support = my_profile.supports.all()
        my_companies_oppose = my_profile.opposes.all()
        my_products_buy = my_profile.buy.all()
        my_products_dontbuy = my_profile.dontbuy.all()
        #if not message:
        #    message = 'Welcome back Boycotter!'
        return render_to_response('frontpage_auth.html',
            {'message':message,
            'user':request.user,
            'campaigns':my_campaigns,
            'companies_support':my_companies_support,
            'companies_oppose':my_companies_oppose,
            'products_buy':my_products_buy,
            'products_dontbuy':my_products_dontbuy},
            context_instance = RequestContext(request))
        
def highlight_campaign_view(request,slug):
    name = deslug(slug)
    campaign = get_object_or_404(Campaign,name__iexact=name)
    print campaign
    if campaign.highlight:
        return redirect(campaign)
    else:
        raise Http404

def search_view(request):
    '''The non-ajax search view'''
    query = request.GET.get('q', '')
    results = {}
    if query:
        results['products'] = Product.objects.filter(name__icontains=query)
        results['companies'] = Company.objects.filter(name__icontains=query)
        results['locations'] = Location.objects.filter(name__icontains=query)
    return render_to_response('search.html',
        {'query':query,'results':results},
        context_instance = RequestContext(request))
        