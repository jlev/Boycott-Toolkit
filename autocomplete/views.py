from django.http import HttpResponse
from django.core import serializers
from tagging.models import Tag
from django.db.models import get_model

def list_objects(request,model):
    '''Query the objects saved for a particular model'''
    try:
        (app_label,model_name) = model.split(".")
    except ValueError:
        return HttpResponse('Need full model name with app prefix')
    model_class = get_model(app_label,model_name)
    #check for abstract
    #find subclasses
    
    if model_class == None:
        return HttpResponse('Model "%s.%s" does not exist' % (app_label,model_name))
    try:
        query = request.GET['q']
    except KeyError:
        return HttpResponse("No query string", mimetype='text/plain')
    objects = model_class.objects.filter(name__istartswith=query).values_list('name', flat=True)
    return HttpResponse('\n'.join(objects), mimetype='text/plain')
    
def list_fields(request,model_name):
    '''List the fields available for a particular model'''
    try:
        (app_label,model_name) = model.split(".")
    except ValueError:
        return HttpResponse('Need full model name with app prefix')
    model_class = get_model(app_label,model_name)
    model_fields = model_class._meta._fields() #uses internal api, but should continue to work
    model_fields.pop(0) #drop the pk
    response = []
    for f in model_fields:
        response.append(f.name)
    return HttpResponse('\n'.join(response))