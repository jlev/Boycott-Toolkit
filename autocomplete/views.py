from django.http import HttpResponse
from django.utils import simplejson as json
from tagging.models import Tag
from django.db.models import get_model,Q

from urllib2 import urlopen
from geopy import geocoders

from target.models import Product,Company,Store
from geography.models import Map
from tagging.models import Tag,TaggedItem

def main_search_ajax(request):
    '''The AJAX search view'''
    try:
        query = request.GET['q']
    except KeyError:
        return HttpResponse("No query string", mimetype='text/plain')
    products = Product.objects.filter(Q(name__icontains=query))
    tag = Tag.objects.filter(name__istartswith=query)
    products_by_tag = TaggedItem.objects.get_by_model(Product,tag)
    products_by_company = Product.objects.filter(company__name__icontains=query)
    
    companies = Company.objects.filter( Q(name__icontains=query) |
                                        Q(product=products) |
                                        Q(map__name__icontains=query)
                                      ).distinct()
    locations = Company.objects.filter(address__icontains=query)
    stores = Store.objects.filter(Q(address__icontains=query)|Q(name__icontains=query))
    
    r = []
    r.append("<div class='ac_header'>Companies</div>")
    for c in companies:
        r.append("%s|%s" % (c.name,c.get_absolute_url()))
        
    r.append("<div class='ac_header'>Products</div>")
    for p in products:
        r.append("%s|%s" % (p.name,p.get_absolute_url()))
    for p in products_by_tag:
        r.append("%s tagged '%s'|%s" % (p.name,tag[0].name,p.get_absolute_url()))
    for p in products_by_company:
        r.append("%s sold by %s|%s" % (p.name,p.company.name,p.get_absolute_url()))
    
    r.append("<div class='ac_header'>Stores</div>")
    for s in stores:
        address = s.address.replace('\n',',')
        #convert linebreaks to commas
        address = address.replace('\r','')
        #remove feed returns 
        r.append("%s:%s|%s" % (s.name,address,s.get_absolute_url()))
        
    r.append("<div class='ac_header'>Locations</div>")
    for l in locations:
        address = l.address.replace('\n',',')
        #convert linebreaks to commas
        address = address.replace('\r','')
        #remove feed returns 
        r.append("%s|%s" % (address,l.get_absolute_url()))

    return HttpResponse('\n'.join(r), mimetype='text/plain')
    
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
    
def list_fields(request,model):
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
    
def list_entries(request,model,field):
    '''List the entries already saved for a field'''
    try:
        (app_label,model_name) = model.split(".")
    except ValueError:
        return HttpResponse('Need full model name with app prefix')
    model_class = get_model(app_label,model_name)
    
    try:
        query = request.GET['q']
    except KeyError:
        return HttpResponse("No query string", mimetype='text/plain')
    
    filter_arg = '%s__istartswith' % (field)
    kwargs = {str(filter_arg):str(query)}
    print kwargs
    entries = model_class.objects.values_list(field).filter(**kwargs)
    response = []
    for e in entries:
        response.append(e[0])
    return HttpResponse('\n'.join(response))
    
def geocode(request):
    try:
        query = request.GET['q']
    except KeyError:
        return HttpResponse("No query string", mimetype='text/plain')
        
    r = []
    #first check groundtruth
    gt = urlopen('http://groundtruth.media.mit.edu/search/?q=%s' % query)
    r.append(gt.read())
    
    #check google
    GMAPS_API_KEY = "ABQIAAAAT9uyY_WHXEyDYZHQMelCKhRlte5-xCx01c0gtBmqgDnMLJYMmRS1vGz6k_iWjoIXmQBGNhXYV2UXBQ"
    try:
        r.append("<div class='ac_header'>Google Results</div>")
        g = geocoders.Google(GMAPS_API_KEY)
        place, (lat, lng) = g.geocode(query)
        #transform the response into geojson, just like groundtruth
        geo = {}
        geo['type']='Feature'
        geo['crs'] = dict(properties=dict(name='EPSG:4326'))
        the_geom = {}
        the_geom['coordinates'] = [0,0]
        the_geom['coordinates'][0] = lng
        the_geom['coordinates'][1] = lat
        geo['geometry']=the_geom
        r.append("%s|x|%s" % (place,json.dumps(geo)))
    except ValueError:
        pass
    return HttpResponse('\n'.join(r), mimetype='text/plain') 