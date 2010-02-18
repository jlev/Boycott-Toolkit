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
        message = "We don't have a company by that name. Would you like to add it?"
        return render_to_response('targets/company_list.html',
               {'message':message,
               'companies':c},
               context_instance = RequestContext(request))
    if len(c) > 1:
        #we got more than one, user needs to filter down
        message = "These are the companies we track that start with " + name + ":"
        return render_to_response('targets/company_list.html',
               {'message':message,
               'companies':c},
               context_instance = RequestContext(request))
    else:
        #there's only one
        c = c[0]
        p = Product.objects.filter(company=c)
        return render_to_response('targets/company_single.html',
            {'company':c,'logo_img':c.logo,'products':p},
            context_instance = RequestContext(request))

@login_required
def company_edit(request,slug):
    name = deslug(slug)
    company = Company.objects.get_or_create(name__iexact=name)
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            company = form.save()
            return render_to_response('targets/company_single.html',
                {'message':"Thanks for adding this company to the database",
                'company':company},
                context_instance = RequestContext(request))
    else:
        form = CompanyForm(instance=company)
        return render_to_response("targets/company_edit.html",
                        {"form": form},
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
        message = "We don't have any products by that name. Would you like to add it?"
        return render_to_response('targets/product_list.html',
               {'message':message,
               'products':p},
               context_instance = RequestContext(request))
    if len(p) > 1:
        #we got more than one, user needs to filter down
        message = "These are the products we track that start with " + name + ":"
        return render_to_response('targets/product_list.html',
               {'message':message,
               'products':p},
               context_instance = RequestContext(request))
    else:
        #there's only one
        p = p[0]
        return render_to_response('targets/product_single.html',
            {'product':p,
            'logo_img_src':p.image.thumbnail.url(),
            'logo_img_width':p.image.thumbnail.width,'logo_img_height':p.image.thumbnail.height},
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

def tag_view(request,tag):
    tag = get_object_or_404(Tag,name__iexact=tag)
    return render_to_response("targets/tags_list.html",{'tag':tag,
        'message':"We track the following items tagged " + tag.name},
    context_instance = RequestContext(request))