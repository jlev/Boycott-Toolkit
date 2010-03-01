from django.http import HttpResponse,HttpResponseNotFound
from django.template import RequestContext
from django.shortcuts import render_to_response,get_object_or_404,get_list_or_404
from django.contrib.auth.decorators import login_required
from boycott.views import deslug

from target.models import Company,Product,Campaign
from target.forms import CompanyForm,ProductForm,CampaignForm
from tagging.models import Tag,TaggedItem

def company_view_all(request):
    #TODO paginate
    c = Company.objects.all()
    return render_to_response('targets/company_list.html',
        {'message':"These are all the companies we currently track:",
        'companies':c},
        context_instance = RequestContext(request))

def company_view(request,slug):
    name = deslug(slug)
    c = Company.objects.filter(name__istartswith=name)
    if len(c) == 0:
        #there isn't one, add it?
        message = "We don't have a company named %s. Would you like to add it?" % name
        return company_add(request,message)
    if len(c) > 1:
        #we got more than one, user needs to filter down
        message = "These are the companies we track that start with %s:" % name
        return render_to_response('targets/company_list.html',
               {'message':message,
               'companies':c},
               context_instance = RequestContext(request))
    else:
        #there's only one
        c = c[0]
        p = Product.objects.filter(company=c)
        return render_to_response('targets/company_single.html',
            {'company':c,
            'logo_img':c.logo.thumbnail,
            'products':p},
            context_instance = RequestContext(request))

@login_required
def company_edit(request,slug):
    name = deslug(slug)
    company = Company.objects.get(name__iexact=name)
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            company = form.save()
            company.edited_by.add(request.user)
            company.save()
            return render_to_response('targets/company_single.html',
                {'message':"Thanks for updating the entry for %s" % company.name,
                'company':company},
                context_instance = RequestContext(request))
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
            company.added_by = request.user
            company.save()
            return render_to_response('targets/company_single.html',
                {'message':"Thanks for adding %s to our database" % company.name,
                'company':company},
                context_instance = RequestContext(request))
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
    name = deslug(slug)
    p = Product.objects.filter(name__istartswith=name)
    if len(p) == 0:
        #there isn't one, add it?
        message = "We don't have a product named %s. Would you like to add it?" % name
        return product_add(request,message)
    if len(p) > 1:
        #we got more than one, user needs to filter down
        message = "These are the products we track that start with %s:" % name
        return render_to_response('targets/product_list.html',
               {'message':message,
               'products':p},
               context_instance = RequestContext(request))
    else:
        #there's only one
        p = p[0]
        return render_to_response('targets/product_single.html',
            {'product':p,
            'logo_img':p.image.thumbnail},
            context_instance = RequestContext(request))
            

@login_required
def product_edit(request,slug):
    name = deslug(slug)
    product = Product.objects.get(name__iexact=name)
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            product.edited_by.add(request.user)
            product.save()
            return render_to_response('targets/company_single.html',
                {'message':"Thanks for updating the entry for %s" % product.name,
                'product':product},
                context_instance = RequestContext(request))
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
            return render_to_response('targets/product_single.html',
                {'message':"Thanks for adding %s to our database" % product.name,
                'product':product},
                context_instance = RequestContext(request))
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
    name = deslug(slug)
    campaign = get_object_or_404(Campaign,name__iexact=name)
    users = campaign.users_joined_campaign
    products = campaign.products.get_query_set()
    companies = campaign.companies.get_query_set()
    return render_to_response("targets/campaign_single.html",
        {'campaign':campaign,'users':users,'products':products,'companies':companies},
        context_instance = RequestContext(request))


@login_required
def campaign_edit(request,slug):
    name = deslug(slug)
    campaign = Campaign.objects.get(name__iexact=name)
    if request.method == 'POST':
        form = CampaignForm(request.POST)
        if form.is_valid():
            campaign = form.save()
            campaign.edited_by.add(request.user)
            campaign.save()
            return render_to_response('targets/campaign_single.html',
                {'message':"Thanks for updating the entry for %s" % campaign.name,
                'campaign':campaign},
                context_instance = RequestContext(request))
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
            campaign.added_by = request.user
            campaign.save()
            return render_to_response('targets/campaign_single.html',
                {'message':"Thanks for starting the %s campaign" % campaign.name,
                'campaign':campaign},
                context_instance = RequestContext(request))
        else:
            return render_to_response('targets/campaign_add.html',
                {'message':"Please correct the errors below",
                "form":form},
                context_instance = RequestContext(request))
    else:
        form = ProductForm()
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