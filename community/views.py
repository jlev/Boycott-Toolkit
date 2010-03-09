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
    redirect_to = request.REQUEST.get('next')
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # Light security check -- make sure redirect_to isn't garbage.
            if not redirect_to or '//' in redirect_to or ' ' in redirect_to:
                redirect_to = settings.LOGIN_REDIRECT_URL
            from django.contrib.auth import login
            login(request, form.get_user())
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
            return HttpResponseRedirect(redirect_to)
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
            form.save(**opts) #create the user object
            user = User.objects.get(username=form.cleaned_data['username'])
            User.set_password(user,form.cleaned_data['password']) #hash password for the database
            #log in immediately
            #should use authenticate() here to set backend automatically
            #but that seems to conflict with facebook connect
            #so do it manually
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
    my_profile = u.profile
    #TODO, upgrade this to actions
    my_campaigns = my_profile.campaigns.all()
    my_companies_support = my_profile.supports.all()
    my_companies_oppose = my_profile.opposes.all()
    my_products_buy = my_profile.buy.all()
    my_products_dontbuy = my_profile.dontbuy.all()
    return render_to_response('community/user_single.html',
        {'the_user':u, #don't use "user", because that will overwrite the request context user
        'campaigns':my_campaigns,
        'companies_support':my_companies_support,
        'companies_oppose':my_companies_oppose,
        'products_buy':my_products_buy,
        'products_dontbuy':my_products_dontbuy},
        context_instance = RequestContext(request))