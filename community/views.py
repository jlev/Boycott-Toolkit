from django.http import HttpResponse,HttpResponseNotFound,HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response,get_object_or_404,get_list_or_404
from django.core.urlresolvers import reverse

from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import Site

from django.contrib.auth.models import User

from community.forms import RegistrationForm
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from django.views.decorators.cache import never_cache

@never_cache
def login_view(request):
    "Displays the login form and handles the login action."
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
            return HttpResponseRedirect("/")
        else:
            print "Invalid Login"
    else:
        form = AuthenticationForm(request)
    request.session.set_test_cookie()
    return render_to_response("registration/login.html", {'form': form}, context_instance=RequestContext(request))

def logout_view(request):
    logout(request)
    #clear cache?
    return HttpResponseRedirect("/")
    
@login_required
def change_password_view(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("login_view"))
    else:
        form = PasswordChangeForm(request.user)
    return render_to_response(template_name, {
        'form': form,
    }, context_instance=RequestContext(request))

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            opts = {}
            opts['use_https'] = request.is_secure()
            opts['email_template_name'] = 'registration/registration_email.txt'
            form.save(**opts)
            #login immediately
            user = User.objects.get(username=form.cleaned_data['username'])
            #supposed to use authenticate() here to set backend, but that seems to conflict with facebook connect
            user.backend='django.contrib.auth.backends.ModelBackend'
            login(request, user)
            return HttpResponseRedirect('/')
    else:
        form = RegistrationForm()
    
    return render_to_response('registration/registration_form.html',
                              {'form': form},
                              RequestContext(request))

def xd_receiver(request):
    '''For Facebook login'''
    return render_to_response('facebook/xd_receiver.html')

def user_view_all(request):
    u = User.objects.all()
    #TODO paginate
    return render_to_response('community/user_list.html',
        {'users':u},
        context_instance = RequestContext(request))

@login_required
def user_view(request,username):
    u = get_object_or_404(User,username=username)
    c = u.profile.campaigns
    return render_to_response('community/user_single.html',
        {'user':u,'campaigns':c},
        context_instance = RequestContext(request))
    
@login_required
def user_campaign_view(request,username):
    return render_to_response("base.html",{'message':"user campaign view not yet implemented"},
        context_instance = RequestContext(request))
    
@login_required
def user_cart_view(request,username):
    u = get_object_or_404(User,username=username)
    c = u.profile.campaigns.all()
    return render_to_response("base.html",{'message':"user cart view not yet implemented"},
        context_instance = RequestContext(request))