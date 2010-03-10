# Create your views here.

def location_by_name(request,slug):
    #TODO: implement location view
    return render_to_response("base.html",{'message':"location by name view not yet implemented"},
        context_instance = RequestContext(request))

def map(request):
    #TODO: implement map view
    return render_to_response("base.html",{'message':"map view not yet implemented"},
        context_instance = RequestContext(request))
    