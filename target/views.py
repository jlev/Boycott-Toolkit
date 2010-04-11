from django.http import HttpResponse,HttpResponseNotFound,HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response,get_object_or_404,get_list_or_404
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import slugify

from django.contrib.gis.geos import Point
from django.contrib.gis.gdal import SpatialReference
from django.utils import simplejson as json
from tagging.models import Tag,TaggedItem

from target.models import Company,Product,Campaign,Store
from target.models import ProductAction,CompanyAction
from info.models import Citation,citation_from_json
from info.views import citations_for_object
from target.forms import CampaignForm,CompanyForm,ProductForm,StoreForm
from target.forms import CompanyActionForm,ProductActionForm
from target.forms import CompanyActionInlineForm,ProductActionInlineForm
from geography.models import Map
from geography.forms import MapInlineForm
from geography.views import geojson_base

def company_view_all(request):
    #TODO paginate
    c = Company.objects.all()
    return render_to_response('targets/company_list.html',
        {'message':"All the companies we currently track:",
        'companies':c},
        context_instance = RequestContext(request))

def company_view(request,slug,message=None):
    c = Company.objects.get(slug=slug)
    p = Product.objects.filter(company=c)
    cites = citations_for_object(c)
    
    try:
        logo_img = c.logo.thumbnail
    except AttributeError:
        logo_img = None
    return render_to_response('targets/company_single.html',
        {'company':c,
        'citations':cites,
        'logo_img':logo_img,
        'products':p,
        'message':message},
        context_instance = RequestContext(request))

@login_required
def company_edit(request,slug):
    company = Company.objects.get(slug=slug)
    if request.POST:
        company_form = CompanyForm(request.POST,request.FILES,instance=company)
        if company_form.is_valid():
            company = company_form.save()
            company.edited_by.add(request.user)
            company.save()
            #save the citations
            citation_from_json(request.POST['citations_json'],company)
            return HttpResponseRedirect(company.get_absolute_url())
        else:
            message = "Please correct the errors below"
    else:
        company_form = CompanyForm(instance=company)
        message = "Edit the company details below"
    return render_to_response("targets/company_edit.html",
                    {"company_form": company_form,
                    "message":message},
    context_instance = RequestContext(request))
        
@login_required
def company_add(request,message=None):
    if request.POST:
        company_form = CompanyForm(request.POST,request.FILES,prefix="company")
        action_form = CompanyActionInlineForm(request.POST,prefix="action")
        map_form = MapInlineForm(request.POST,prefix="map")
        if company_form.is_valid() and map_form.is_valid():
            company = company_form.save()
            company.added_by = request.user #set the user who created it
            company.slug = slugify(company.name) #set the slug
            
            map_form.name = company.name
            #coords are like "lat,lon", need to be converted to real Point object
            coords = map_form.cleaned_data['center'].split(',')
            map_form.cleaned_data['center'] = Point(float(coords[0]),float(coords[1]),srid=4326)
            map = map_form.save()
            company.map = map #set the map

            #send the new company to the other forms
            if action_form.is_valid():
                #send the new product to the action form
                action = action_form.save()
                action.company = company
                action.save()

            #resave the company to finish up
            company.save()
            #save the citations
            citation_from_json(request.POST['company-citations_json'],company)
            return HttpResponseRedirect(company.get_absolute_url())
        else:
            message = "Please correct the errors below"
    else:
        company_form = CompanyForm(prefix='company')
        action_form = CompanyActionInlineForm(prefix='action')
        map_form = MapInlineForm(prefix="map")
        message = "Add the company details below"
    return render_to_response("targets/company_add.html",
                    {"message":message,
                    "company_form":company_form,
                    "action_form":action_form,
                    "map_form":map_form},
    context_instance = RequestContext(request))
        
def product_view_all(request):
    p = Product.objects.all()
    return render_to_response('targets/product_list.html',
        {'message':"All the products we currently track:",
        'products':p},
        context_instance = RequestContext(request))
        
def product_view(request,slug):
    p = get_object_or_404(Product,slug=slug)
    cites = citations_for_object(p)
    try:
        logo_img = p.image.thumbnail
    except AttributeError:
        logo_img = None
   
#    #Determine whether the product is "good" or "bad"
#    actions = ProductAction.objects.filter(product=p)
#    i = 0
#    for a in actions:
#        if a.positive(): i += 1
#        else: i -= 1
#    if (i > 0): 
#        logo_overlay = "green" #it's positive, display green circle
#    else:
#        if i < 0:
#            logo_overlay = "slash" #it's not, display red slash
#        else: 
#            logo_overlay = None #it's neither, or there are no actions, just display the logo
    
    return render_to_response('targets/product_single.html',
        {'product':p,
        'citations':cites,
        'logo_img':logo_img}, #'logo_overlay':logo_overlay},
        context_instance = RequestContext(request))
        

def product_upc(request,upc):
    p = get_object_or_404(Product,upc=upc)
    cites = citations_for_object(p)
    try:
        logo_img = p.image.thumbnail
    except AttributeError:
        logo_img = None

    return render_to_response('targets/product_single.html',
        {'product':p,
        'citations':cites,
        'logo_img':logo_img},
        context_instance = RequestContext(request))
@login_required
def product_edit(request,slug):
    product = get_object_or_404(Product,slug=slug)
    if request.POST:
        product_form = ProductForm(request.POST,request.FILES,instance=product)
        if product_form.is_valid():
            product = product_form.save()
            product.edited_by.add(request.user)
            product.save()
            #save the citations
            citation_from_json(request.POST['citations_json'],product)
            return HttpResponseRedirect(product.get_absolute_url())
        else:
            message = "Please correct the errors below"
    else:
        product_form = ProductForm(instance=product)
        message = "Edit the product details below"
    return render_to_response("targets/product_edit.html",
                    {"message":message,"product_form": product_form},
    context_instance = RequestContext(request))

@login_required
def product_add(request,message=None):
    if request.POST:
        product_form = ProductForm(request.POST,request.FILES,prefix='product')
        action_form = ProductActionInlineForm(request.POST,prefix='action')
        if product_form.is_valid():
            product = product_form.save()
            #set the user who added it
            product.added_by = request.user
            #set the slug
            product.slug = slugify(product.name)
            
            if action_form.is_valid():
                #send the new product to the action form
                action = action_form.save()
                action.product = product
                action.save()
            #resave the product to finish up
            product.save()
            #save the citations
            citation_from_json(request.POST['product-citations_json'],product)
            return HttpResponseRedirect(product.get_absolute_url())
        else:
           message = "Please correct the errors below"
    else:
        product_form = ProductForm(prefix='product')
        action_form = ProductActionInlineForm(prefix='action')
        message = "Add the product details below"
    return render_to_response("targets/product_add.html",
                    {"product_form": product_form,
                    "action_form":action_form,
                    "message":message},
    context_instance = RequestContext(request))
            
def campaign_view_all(request):
    c = Campaign.objects.all()
    return render_to_response('targets/campaign_list.html',
        {'message':"All the campaigns which are currently running:",
        'campaigns':c},
        context_instance = RequestContext(request))

def campaign_view(request,slug):
    campaign = get_object_or_404(Campaign,slug=slug)
    campaign_users = campaign.users_joined_campaign.get_query_set()
    cites = citations_for_object(campaign)
    if not request.user.is_anonymous():
        user_joined_campaign = (campaign in request.user.profile.campaigns.all())
    else:
        user_joined_campaign = False 
    product_actions = campaign.productaction_set.get_query_set()
    company_actions = campaign.companyaction_set.get_query_set()
    
    return render_to_response("targets/campaign_single.html",
        {'campaign':campaign,'citations':cites,
        'campaign_users':campaign_users,'user_joined_campaign':user_joined_campaign,
        'product_actions':product_actions,'company_actions':company_actions},
        context_instance = RequestContext(request))


@login_required
def campaign_edit(request,slug):
    campaign = Campaign.objects.get(slug=slug)
    if request.POST:
        form = CampaignForm(request.POST,instance=campaign)
        if form.is_valid():
            campaign = form.save()
            campaign.edited_by.add(request.user)
            campaign.save()
            #save the citations
            citation_from_json(request.POST['citations_json'],campaign)
            return HttpResponseRedirect(campaign.get_absolute_url())
        else:
            message = "Please correct the errors below"
    else:
        form = CampaignForm(instance=campaign)
        message = "Edit the campaign details below"
    return render_to_response("targets/campaign_edit.html",
                    {"message":message,"form": form},
                    context_instance = RequestContext(request))

@login_required
def campaign_add(request,message=None):
    if request.POST:
        form = CampaignForm(request.POST)
        if form.is_valid():
            campaign = form.save()
            #set the user who added it
            campaign.added_by = request.user
            #set the slug
            campaign.slug = slugify(campaign.name)
            campaign.save()
            #save the citations
            citation_from_json(request.POST['citations_json'],campaign)
            return HttpResponseRedirect(campaign.get_absolute_url())
        else:
            message = "Please correct the errors below"
    else:
        form = CampaignForm()
        message = "Add the campaign details below"
    return render_to_response("targets/campaign_add.html",
                    {"message":message,"form": form},
                    context_instance = RequestContext(request))

@login_required
def campaign_add_product(request,slug):
    campaign = Campaign.objects.get(slug=slug)
    if request.POST:
        form = ProductActionForm(request.POST)
        if form.is_valid():
            product_action = form.save()
            print "saved",product_action
            return HttpResponseRedirect(campaign.get_absolute_url())
        else:
            message = "Please correct the errors below"
    else:
        action = ProductAction(campaign=campaign)
        form = ProductActionForm(instance=action)
        message = "Edit the product action details below"
    return render_to_response("targets/campaign_add_product.html",
                    {"message":message,"form": form,
                    'campaign':campaign},
                    context_instance = RequestContext(request))
                    
@login_required
def campaign_add_company(request,slug):
    campaign = Campaign.objects.get(slug=slug)
    if request.method == 'POST':
        form = CompanyActionForm(request.POST)
        if form.is_valid():
            company_action = form.save()
            return HttpResponseRedirect(campaign.get_absolute_url())
        else:
            message = "Please correct the errors below"
    else:
        action = CompanyAction(campaign=campaign) #create a temp object to prefill the campaign
        form = CompanyActionForm(instance=action)
        message = "Edit the company action details below"
    return render_to_response("targets/campaign_add_company.html",
                    {"message":message,"form": form,
                    'campaign':campaign},
                    context_instance = RequestContext(request))
                    
@login_required
def user_join_campaign(request,slug):  
    if request.method == "POST":
        campaign = Campaign.objects.get(slug=slug)
        request.user.profile.campaigns.add(campaign)
        return HttpResponse("%s joined %s" % (request.user,campaign))
    else:
        return HttpResponse("don't try to GET a url that changes state")
    
@login_required
def user_leave_campaign(request,slug):
    if request.method == "POST":
        campaign = Campaign.objects.get(slug=slug)
        request.user.profile.campaigns.remove(campaign)
        return HttpResponse("%s left %s" % (request.user,campaign))
    else:
        return HttpResponse("don't try to GET a url that changes state")
    

def store_view_all(request):
    all_stores = Store.objects.all()
    #hardcode to continental US
    usa = Map.objects.get(name="United States")
    return render_to_response("targets/store_map.html",{
        'stores':all_stores,
        'map':usa,},
        context_instance = RequestContext(request))

def store_view(request,slug):
    s = Store.objects.get(slug=slug)
    p = s.products

    try:
        logo_img = s.logo.thumbnail
    except AttributeError:
        logo_img = None
    return render_to_response('targets/store_single.html',
        {'store':s,
        'logo_img':logo_img,
        'products':p},
        context_instance = RequestContext(request))
     
def store_all_json(request):
    obj = {}
    obj['type']='FeatureCollection'
    obj['features'] = []
    
    stores = Store.objects.all()
    for store in stores:
        properties = {}
        properties['name'] = store.name
        properties['address'] = store.address
        properties['id'] = store.id
        geojson = geojson_base(SpatialReference('EPSG:900913'),store.location,properties)
        obj['features'].append(geojson)
    return HttpResponse(json.dumps(obj))
     
@login_required
def store_add(request,message=None):
    if request.POST:
        store_form = StoreForm(request.POST,prefix="store")
        map_form = MapInlineForm(request.POST,prefix="map")
        if store_form.is_valid() and map_form.is_valid():
            store = store_form.save()
            
            #coords are like "lat,lon", need to be converted to real Point object
            coords = map_form.cleaned_data['center'].split(',')
            map_form.cleaned_data['center'] = Point(float(coords[0]),float(coords[1]),srid=4326)
            map = map_form.save()
            store.location = map.center
            
            #set the user who added it
            store.added_by = request.user
            #set the slug
            store.slug = slugify(store.name+"-"+map.name)
            store.save()
            #save the citations
            #citation_from_json(request.POST['citations_json'],store)
            return HttpResponseRedirect(store.get_absolute_url())
        else:
            message = "Please correct the errors below"
    else:
        store_form = StoreForm(prefix="store")
        map_form = MapInlineForm(prefix="map")
        message = "Add the store details below"
    return render_to_response("targets/store_add.html",
                    {"message":message,"store_form": store_form,"map_form":map_form},
                    context_instance = RequestContext(request))

@login_required
def store_edit(request,slug):
    store = Store.objects.get(slug=slug)
    if request.POST:
        form = StoreForm(request.POST,instance=store)
        if form.is_valid():
            store = form.save()
            store.edited_by.add(request.user)
            store.save()
            return HttpResponseRedirect(store.get_absolute_url())
        else:
            message = "Please correct the errors below"
    else:
        form = StoreForm(instance=store)
        message = "Edit the campaign details below"
    return render_to_response("targets/store_edit.html",
                    {"message":message,"form": form},
                    context_instance = RequestContext(request))

def tag_view(request,tag):
    tag = get_object_or_404(Tag,name__iexact=tag)
    return render_to_response("targets/tags_list.html",{'tag':tag,
        'message':"We track the following items tagged " + tag.name},
    context_instance = RequestContext(request))