from django.http import HttpResponse,HttpResponseNotFound
from django.template import RequestContext
from django.shortcuts import render_to_response,get_object_or_404,redirect
from django.views.decorators.cache import cache_control

from django.contrib.auth.models import User
from target.models import Campaign,Product,Company,CompanyAction,ProductAction
from geography.models import Location

def frontpage_view(request,message=None):
    campaigns = Campaign.objects.filter(highlight=True)
    product_actions = ProductAction.objects.filter(campaign__in=campaigns)
    company_actions = CompanyAction.objects.filter(campaign__in=campaigns)
    
    return render_to_response('frontpage.html',
        {'message':message,
        'campaigns':campaigns,
        'product_actions':product_actions,
        'company_actions':company_actions},
        context_instance = RequestContext(request))
        
def highlight_campaign_view(request,slug):
    campaign = get_object_or_404(Campaign,slug=slug) #raises 404 if none found
    if campaign.highlight:
        return redirect(campaign)

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
        