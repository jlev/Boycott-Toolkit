from django.http import HttpResponse,HttpResponseNotFound
from django.template import RequestContext
from django.shortcuts import render_to_response,get_object_or_404
from django.db.models import get_model

from info.models import Source,Citation

def source_view(request,id):
    source = Source.objects.filter(id=id)
    citations = Citation.objects.filter(source=source)
    return render_to_response('info/source_single.html',
        dict(layer=l,name=name,citations=citations),
        context_instance = RequestContext(request))