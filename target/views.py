from django.http import HttpResponse,HttpResponseNotFound,HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response,get_object_or_404,get_list_or_404
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import slugify

from target.models import Company,Product,Campaign,ProductAction,CompanyAction
from target.forms import CampaignForm,CompanyForm,ProductForm
from target.forms import CompanyActionForm,ProductActionForm
from target.forms import CompanyActionInlineForm,ProductActionInlineForm
from geography.forms import MapInlineForm
from django.contrib.gis.geos import Point
from tagging.models import Tag,TaggedItem

def company_view_all(request):
    #TODO paginate
    c = Company.objects.all()
    return render_to_response('targets/company_list.html',
        {'message':"These are all the companies we currently track:",
        'companies':c},
        context_instance = RequestContext(request))

def company_view(request,slug,message=None):
    c = Company.objects.get(slug=slug)
    p = Product.objects.filter(company=c)
    
    try:
        logo_img = c.logo.thumbnail
    except AttributeError:
        logo_img = None
    return render_to_response('targets/company_single.html',
        {'company':c,
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
        if company_form.is_valid() and action_form.is_valid() and map_form.is_valid():
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
            action_form.cleaned_data['company'] = company
            action = action_form.save()
            #TODO, set action_form with new company_id

            #resave the company to finish up
            company.save()
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
        {'message':"These are all the products we currently track:",
        'products':p},
        context_instance = RequestContext(request))
        
def product_view(request,slug):
    p = Product.objects.get(slug=slug)
    try:
        logo_img = p.image.thumbnail
    except AttributeError:
        logo_img = None
   
    #Determine whether the product is "good" or "bad"
    actions = ProductAction.objects.filter(product=p)
    i = 0
    for a in actions:
        if a.positive(): i += 1
        else: i -= 1
    if (i > 0): 
        logo_overlay = "green" #it's positive, display green circle
    else:
        if i < 0:
            logo_overlay = "slash" #it's not, display red slash
        else: 
            logo_overlay = None #it's neither, or there are no actions, just display the logo
    
    return render_to_response('targets/product_single.html',
        {'product':p,
        'logo_img':logo_img,'logo_overlay':logo_overlay},
        context_instance = RequestContext(request))
        

@login_required
def product_edit(request,slug):
    product = Product.objects.get(slug=slug)
    if request.POST:
        product_form = ProductForm(request.POST,request.FILES,instance=product)
        if product_form.is_valid():
            product = product_form.save()
            product.edited_by.add(request.user)
            product.save()
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
            product.save()
            #send the new product to the action form
            #action_form.product = product
            
            if action_form.is_valid():
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
        {'message':"These are all the campaigns we are currently running:",
        'campaigns':c},
        context_instance = RequestContext(request))

def campaign_view(request,slug):
    campaign = get_object_or_404(Campaign,slug=slug)
    users = campaign.users_joined_campaign
    product_actions = campaign.productaction_set.get_query_set()
    company_actions = campaign.companyaction_set.get_query_set()
    
    return render_to_response("targets/campaign_single.html",
        {'campaign':campaign,'users':users,'product_actions':product_actions,'company_actions':company_actions},
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
        print "POST"
        if form.is_valid():
            print "valid form"
            company_action = form.save()
            print "saved",company_action
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

def store_view_all(request):
    #TODO: implement location view
    return render_to_response("base.html",{'message':"store view not yet implemented"},
        context_instance = RequestContext(request))

def tag_view(request,tag):
    tag = get_object_or_404(Tag,name__iexact=tag)
    return render_to_response("targets/tags_list.html",{'tag':tag,
        'message':"We track the following items tagged " + tag.name},
    context_instance = RequestContext(request))