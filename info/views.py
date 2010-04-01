from django.http import HttpResponse,HttpResponseNotFound
from django.template import RequestContext
from django.shortcuts import render_to_response,get_object_or_404
from django.db.models import get_model
from django.contrib.contenttypes.models import ContentType

from info.models import Source,Citation
from info.forms import SourceForm,CitationForm

def source_view(request,id):
    source = Source.objects.get(id=id)
    citations = Citation.objects.filter(source=source)
    return render_to_response('info/source_single.html',
        dict(source=source,citations=citations),
        context_instance = RequestContext(request))
        
def citations_for_object(obj):
    '''Get all the citations for a citable object'''
    obj_type = ContentType.objects.get_for_model(obj)
    return Citation.objects.filter(cited_type=obj_type,cited_id=obj.id)

def citations_for_object_field(obj,field):
    '''Get all the citations for a field in a citable object'''
    obj_type = ContentType.objects.get_for_model(obj)
    return Citation.objects.filter(cited_type=obj_type,cited_id=obj.id,cited_field=field)