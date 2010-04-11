from django.http import HttpResponse,HttpResponseNotFound
from django.template import RequestContext
from django.shortcuts import render_to_response

def location_by_name(request,slug):
    #TODO: implement location view
    return render_to_response("base.html",{'message':"location by name view not yet implemented"},
        context_instance = RequestContext(request))

def map(request):
    #TODO: implement map view
    return render_to_response("base.html",{'message':"map view not yet implemented"},
        context_instance = RequestContext(request))

def geojson_base(projection,the_geom,properties):
    '''Returns a geojson compatible dictionary, with coords from geom_field in the specified projection.
    Note that to you still have to turn this into real json with dumps()
    Pass in the geometry field, and a properties dictionary
    Follows GeoJSON 1.0 spec: http://geojson.org/geojson-spec.html'''
    dic = {}
    dic['type']='Feature'
    the_geom.transform(projection) #convert to output proj, works in place but doesn't save to db
    dic['geometry']=eval(the_geom.geojson) #eval is necessary to get rid of string notation
    dic['properties'] = properties
    #create reference system
    dic['crs'] = {'type':'name','properties':{'name':'EPSG:%s' % projection.srid}}
    return dic