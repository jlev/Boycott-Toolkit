from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey
from django.utils import simplejson as json
from django.forms import ValidationError

CITABLE_MODELS = {"model__in": ("company","product","campaign")}

class Source(models.Model):
    '''Where information comes from'''
    name = models.CharField('Name',max_length=100)
    author = models.CharField('Author',max_length=100,null=True,blank=True)
    url = models.URLField(null=True,blank=True)
    date = models.DateField(auto_now=False,null=True,blank=True)
    def __unicode__(self):
        return "%s, %s, %s" % (self.author,self.name,self.date)
    def html(self):
        string = ""
        if self.author: string += (self.author + ", ")
        if (self.name and self.url):
            string += "<i><a href=%s target='_blank'>%s</a></i>" % (self.url,self.name)
        else:
            if self.name:
                string += "<i>%s</i>" % self.name
            if self.url:
                string += "<a href=%s target='_blank'>%s</a>" % (self.url,self.url)
        if self.date:
            string += (", " + str(self.date))
        return string

class Citation(models.Model):
    '''Link a specific field in a particular model to a source'''
    source = models.ForeignKey(Source,null=True)
    cited_type = models.ForeignKey(ContentType,limit_choices_to=CITABLE_MODELS)
    cited_field = models.CharField(max_length=25,blank=True,null=True)
    cited_id = models.PositiveIntegerField(default=0)
    cited_object = GenericForeignKey("cited_type","cited_id")
    apply_to_all = models.BooleanField("Apply this citation to all instances of the model type",default=False)
    def __unicode__(self):
        if self.apply_to_all:
            object_name = self.cited_type
        else:
            object_name = self.cited_type.get_object_for_this_type(id=self.cited_id)
        return '%s %s: %s' % (object_name,self.cited_field, self.source.name)
        
def citation_from_json(json_string,obj):
    '''Create and save citation objects from a json string, with the object to link it to'''
    cited_type = ContentType.objects.get_for_model(obj)
    
    citations = json.loads(json_string)
    for c in citations:
        (source,created) = Source.objects.get_or_create(name=c['title'],author=c['author'],url=c['url'])
        if(c['date'] != ""):
            try:
                source.date = c['date']
            except ValidationError:
                print "could not validate",c['date']
        cite = Citation(source=source,cited_type=cited_type,cited_field=c['field'],cited_id=obj.id)
        cite.save()