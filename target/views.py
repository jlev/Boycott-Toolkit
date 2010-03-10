from django.http import HttpResponse,HttpResponseNotFound,HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response,get_object_or_404,get_list_or_404
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import slugify

from target.models import Company,Product,Campaign,ProductAction,CompanyAction
from target.forms import CompanyForm,ProductForm,CampaignForm,CompanyActionForm,ProductActionInlineForm
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
    if request.method == 'POST':
        form = CompanyForm(request.POST,instance=company)
        if form.is_valid():
            company = form.save()
            company.edited_by.add(request.user)
            company.save()
            return HttpResponseRedirect(company.get_absolute_url())
        else:
            return render_to_response('targets/company_edit.html',
                {'message':"Please correct the errors below",
                "form":form},
                context_instance = RequestContext(request))
    else:
        form = CompanyForm(instance=company)
        return render_to_response("targets/company_edit.html",
                        {"form": form,"message":"Edit the company details below"},
        context_instance = RequestContext(request))
        
@login_required
def company_add(request,message=None):
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            company = form.save()
            #set the user who created it
            company.added_by = request.user
            #set the slug
            company.slug = slugify(company.name)
            company.save()
            return HttpResponseRedirect(company.get_absolute_url())
        else:
            return render_to_response('targets/company_add.html',
                {'message':"Please correct the errors below",
                "form":form},
                context_instance = RequestContext(request))
    else:
        form = CompanyForm()
        if message is None:
            message = "Add the company details below"
        return render_to_response("targets/company_add.html",
                        {"form": form,"message":message},
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
    if request.method == 'POST':
        form = ProductForm(request.POST,instance=product)
        if form.is_valid():
            product = form.save()
            product.edited_by.add(request.user)
            product.save()
            return HttpResponseRedirect(product.get_absolute_url())
        else:
            return render_to_response('targets/product_edit.html',
                {'message':"Please correct the errors below",
                "form":form},
                context_instance = RequestContext(request))
    else:
        form = ProductForm(instance=product)
        return render_to_response("targets/product_edit.html",
                        {"message":"Edit the product details below","form": form},
        context_instance = RequestContext(request))

@login_required
def product_add(request,message=None):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            product.added_by = request.user
            product.save()
            return HttpResponseRedirect(product.get_absolute_url())
        else:
            return render_to_response('targets/product_add.html',
                {'message':"Please correct the errors below",
                "form":form},
                context_instance = RequestContext(request))
    else:
        form = ProductForm()
        if message is None:
            message = "Add the product details below"
        return render_to_response("targets/product_add.html",
                        {"form": form,
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
    if request.method == 'POST':
        form = CampaignForm(request.POST,instance=campaign)
        if form.is_valid():
            campaign = form.save()
            campaign.edited_by.add(request.user)
            campaign.save()
            return HttpResponseRedirect(campaign.get_absolute_url())
        else:
            return render_to_response('targets/campaign_edit.html',
                {'message':"Please correct the errors below",
                "form":form},
                context_instance = RequestContext(request))
    else:
        form = CampaignForm(instance=campaign)
        return render_to_response("targets/campaign_edit.html",
                        {"message":"Edit the campaign details below","form": form},
        context_instance = RequestContext(request))

@login_required
def campaign_add(request,message=None):
    if request.method == 'POST':
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
            return render_to_response('targets/campaign_add.html',
                {'message':"Please correct the errors below",
                "form":form},
                context_instance = RequestContext(request))
    else:
        form = CampaignForm()
        if message is None:
            message = "Add the campaign details below"
        return render_to_response("targets/campaign_add.html",
                        {"message":message,"form": form},
        context_instance = RequestContext(request))


def tag_view(request,tag):
    tag = get_object_or_404(Tag,name__iexact=tag)
    return render_to_response("targets/tags_list.html",{'tag':tag,
        'message':"We track the following items tagged " + tag.name},
    context_instance = RequestContext(request))