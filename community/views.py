from django.http import HttpResponse,HttpResponseNotFound
from django.template import RequestContext
from django.shortcuts import render_to_response,get_object_or_404,get_list_or_404
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User

def xd_receiver(request):
    return render_to_response('registration/xd_receiver.html')

def user_view_all(request):
    u = User.objects.all()
    #TODO paginate
    return render_to_response('community/user_list.html',
        {'users':u},
        context_instance = RequestContext(request))

@login_required
def user_view(request,username):
    u = get_object_or_404(User,username=username)
    return render_to_response('community/user_single.html',
        {'user':u},
        context_instance = RequestContext(request))
        
def campaign_view(request,slug):
    pass