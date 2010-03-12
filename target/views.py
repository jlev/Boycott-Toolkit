from django.http import HttpResponse,HttpResponseNotFound,HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response,get_object_or_404,get_list_or_404
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import slugify

from target.models import Company,Product,Campaign,ProductAction,CompanyAction
from target.forms import CompanyForm,ProductForm,CampaignForm,CompanyActionInlineForm,ProductActionInlineForm
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
        company_form = CompanyForm(request.POST,request.FILES,instance=company)
        if company_form.is_valid():
            company = company_form.save()
            company.edited_by.add(request.user)
            company.save()
            return HttpResponseRedirect(company.get_absolute_url())
        else:
            return render_to_response('targets/company_edit.html',
                {'message':"Please correct the errors below",
                "company_form":company_form},
                context_instance = RequestContext(request))
    else:
        company_form = CompanyForm(instance=company)
        return render_to_response("targets/company_edit.html",
                        {"company_form": company_form,
                        "message":"Edit the company details below"},
        context_instance = RequestContext(request))
        
@login_required
def company_add(request,message=None):
    if request.method == 'POST':
        company_form = CompanyForm(request.POST,request.FILES,prefix="company")
        action_form = CompanyActionInlineForm(request.POST,prefix="action")
        if company_form.is_valid():
            company = company_form.save()
            #set the user who created it
            company.added_by = request.user
            #set the slug
            company.slug = slugify(company.name)
            company.save()
            #send the new company to the action form
            action_form.company = company
            
            if action_form.is_valid():
                return HttpResponseRedirect(company.get_absolute_url())
        else:
            return render_to_response('targets/company_add.html',
                {'message':"Please correct the errors below",
                "company_form":company_form,
                "action_form":action_form},
                context_instance = RequestContext(request))
    else:
        company_form = CompanyForm(prefix='company')
        action_form = CompanyActionInlineForm(prefix='action')
        if message is None:
            message = "Add the company details below"
        return render_to_response("targets/company_add.html",
                        {"message":message,
                        "company_form":company_form,
                        "action_form":action_form},
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
        product_form = ProductForm(request.POST,request.FILES,instance=product)
        if product_form.is_valid():
            product = product_form.save()
            product.edited_by.add(request.user)
            product.save()
            return HttpResponseRedirect(product.get_absolute_url())
        else:
            return render_to_response('targets/product_edit.html',
                {'message':"Please correct the errors below",
                "product_form":product_form},
                context_instance = RequestContext(request))
    else:
        product_form = ProductForm(instance=product)
        return render_to_response("targets/product_edit.html",
                        {"message":"Edit the product details below","product_form": product_form},
        context_instance = RequestContext(request))

@login_required
def product_add(request,message=None):
    if request.method == 'POST':
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
            action_form.product = product
            
            if action_form.is_valid():
                return HttpResponseRedirect(product.get_absolute_url())
        else:
            return render_to_response('targets/product_add.html',
                {'message':"Please correct the errors below",
                "product_form":product_form,
                "action_form":action_form},
                context_instance = RequestContext(request))
    else:
        product_form = ProductForm(prefix='product')
        action_form = ProductActionInlineForm(prefix='action')
        if message is None:
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

def store_view_all(request):
    #TODO: implement location view
    return render_to_response("base.html",{'message':"store view not yet implemented"},
        context_instance = RequestContext(request))

def tag_view(request,tag):
    tag = get_object_or_404(Tag,name__iexact=tag)
    return render_to_response("targets/tags_list.html",{'tag':tag,
        'message':"We track the following items tagged " + tag.name},
    context_instance = RequestContext(request))