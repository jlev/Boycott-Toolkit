from django.http import HttpResponse,HttpResponseNotFound
from django.template import RequestContext
from django.shortcuts import render_to_response,get_object_or_404,redirect
from django.views.decorators.cache import cache_control
import urllib2

from django.contrib.auth.models import User
from target.models import Campaign,Product,Company,CompanyAction,ProductAction

def frontpage_view(request,message=None):
    campaigns = Campaign.objects.select_related('user_joined_campaign').filter(highlight=True)
    product_actions = ProductAction.objects.select_related('product').filter(campaign__in=campaigns)
    company_actions = CompanyAction.objects.select_related('company').filter(campaign__in=campaigns)
    
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
        results['locations'] = Company.objects.filter(address__icontains=query)
    return render_to_response('search.html',
        {'query':query,'results':results},
        context_instance = RequestContext(request))


def proxy(request,theURL):
    """This is a blind proxy that we use to get around browser
    restrictions that prevent the Javascript from loading pages not on the
    same server as the Javascript.  This has several problems: it's less
    efficient, it might break some sites, and it's a security risk because
    people can use this proxy to browse the web and possibly do bad stuff
    with it.  It only loads pages via http and https, but it can load any
    content type. It supports GET requests."""

    # Designed to prevent Open Proxy type stuff.
    allowedHosts = ['groundtruth.media.mit.edu',]

    response = HttpResponse()

    #fix URL percent encoding
    url = theURL.replace('%2F','/')
    url.replace('%3A',':')

    if url == "":
        url = "http://www.example.com"

    try:        
        host = url.split("/")[2]
        if allowedHosts and not host in allowedHosts:
            response.write("Status: 502 Bad Gateway\n")
            response.write("Content-Type: text/plain\n")
            response.write("This proxy does not allow you to access the location (%s).\n" % (host,))

        elif url.startswith("http://") or url.startswith("https://"):
#           if request.method == "POST":
#               length = int(request.META["CONTENT_LENGTH"])
#               headers = {"Content-Type": request.META["CONTENT_TYPE"]}
#               body = sys.stdin.read(length)
#               ##fix
#               r = urllib2.Request(url, body, headers)
#               y = urllib2.urlopen(r)
#           else:
            y = urllib2.urlopen(url)

            i = y.info()
            #Content Type headers seem to mess up OL ajax requests, so forget it
            #if i.has_key("Content-Type"):
            #    response.write("Content-Type: %s" % (i["Content-Type"]))
            #else:
            #    response.write("Content-Type: text/plain\n")
            response.write(y.read())
            y.close()
        else:
            response.write("Content-Type: text/plain\n")
            response.write("Illegal request.\n")

    except Exception, E:
        response.write("Status: 500 Unexpected Error\n")
        response.write("Content-Type: text/plain\n")
        response.write("Some unexpected error occurred. Error text was:\n")
        response.write(str(E))

    return response