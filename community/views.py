from django.http import HttpResponse,HttpResponseNotFound,HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response,get_object_or_404,get_list_or_404
from django.core.urlresolvers import reverse

from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
import facebook.djangofb as facebook
from facebookconnect.models import FacebookProfile
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import Site

from django.contrib.auth.models import User

from community.forms import RegistrationForm
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from django.views.decorators.cache import never_cache

from reversion.models import Revision

from boycott import settings
from target.models import ProductAction,CompanyAction
from community.models import UserProfile
from community.forms import UserProfileForm

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
            #print "Invalid Login"
            pass
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
            return HttpResponseRedirect(reverse("auth_login"))
    else:
        form = PasswordChangeForm(request.user)
    return render_to_response('community/change_password.html', {'form': form}, context_instance=RequestContext(request))

def register_view(request):
    redirect_to = request.REQUEST.get('next')
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
            
            # Light security check -- make sure redirect_to isn't garbage.
            if not redirect_to or '//' in redirect_to or ' ' in redirect_to:
                redirect_to = settings.LOGIN_REDIRECT_URL
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
            return HttpResponseRedirect(redirect_to)
    else:
        form = RegistrationForm()
    
    return render_to_response('registration/registration_form.html',
                              {'form': form},
                              RequestContext(request))

def xd_receiver(request):
    '''For Facebook login'''
    return render_to_response('facebook/xd_receiver.html')

def user_view_all(request):
    u = User.objects.all().order_by("-date_joined")
    #TODO paginate
    return render_to_response('community/user_list.html',
        {'users':u},
        context_instance = RequestContext(request))

def user_view(request,username):
    u = get_object_or_404(User,username=username)
    my_profile = u.profile
    my_campaigns = my_profile.campaigns.all()
    my_product_actions = ProductAction.objects.select_related('product').filter(campaign__in=my_campaigns)
    my_company_actions = CompanyAction.objects.select_related('company').filter(campaign__in=my_campaigns)
    my_revisions = Revision.objects.select_related('version').filter(user=u).order_by("-date_created")[:10]
    
    #clean up list
    return render_to_response('community/user_single.html',
        {'the_user':u, #don't use "user", because that will overwrite the request context user
        'campaigns':my_campaigns,
        'company_actions':my_company_actions,
        'product_actions':my_product_actions,
        'revisions':my_revisions},
        context_instance = RequestContext(request))
        
@login_required
def user_edit(request,username):
    #only let people edit their own profiles
    if request.user.username != username:
        return HttpResponseRedirect(request.user.profile.get_absolute_url() + 'edit')
    
    profile = get_object_or_404(UserProfile,user__username=username)
    if request.POST:
        form = UserProfileForm(request.POST,instance=profile)
        if form.is_valid():
            profile = form.save()
            return HttpResponseRedirect(profile.get_absolute_url())
        else:
            message = "Please correct the errors below"
    else:
        form = UserProfileForm(instance=profile)
        message = "Edit your user profile below"
    return render_to_response("community/user_profile_edit.html",
                    {"message":message,"form": form},
                    context_instance = RequestContext(request))
                    
@facebook.require_login()
def facebook_canvas(request):
    if request.user.is_anonymous():
        #we need to make fb/django connection
        if request.method == "POST":
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                from django.contrib.auth import login
                login(request, form.get_user())
                if request.session.test_cookie_worked():
                    request.session.delete_test_cookie()
                #we're logged in, go ahead with rest of render
        else:
            form = AuthenticationForm(request)
        request.session.set_test_cookie()
        return render_to_response('facebook/please_login.html',{'form': form}, context_instance=RequestContext(request))
    my_profile = request.user.profile
    my_campaigns = my_profile.campaigns.all()
    my_product_actions = ProductAction.objects.select_related('product').filter(campaign__in=my_campaigns)
    my_company_actions = CompanyAction.objects.select_related('company').filter(campaign__in=my_campaigns)
    my_revisions = Revision.objects.select_related('version').filter(user=request.user).order_by("-date_created")[:10]
    
    return render_to_response('community/canvas.fbml',{'campaigns':my_campaigns,
                                                       'company_actions':my_company_actions,
                                                       'product_actions':my_product_actions,
                                                       'revisions':my_revisions},
                                                       context_instance = RequestContext(request))
                                                       
def recent_edits(request):
    edits = Revision.objects.select_related('version').all().order_by("-date_created")[:25]
    return render_to_response('community/recent_edits.html',{'edits':edits},
                                context_instance = RequestContext(request))