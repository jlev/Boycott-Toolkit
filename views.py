from django.http import HttpResponse,HttpResponseNotFound
from django.template import RequestContext
from django.shortcuts import render_to_response,get_object_or_404

def deslug(name):
	bits = name.split('-')
	for i,b in enumerate(bits):
	    bits[i] = b.capitalize()
	return " ".join(bits)

def frontpage_view(request):
    return render_to_response('base.html',
        {'message':"Welcome to the Boycott Toolkit"},
        context_instance = RequestContext(request))
    