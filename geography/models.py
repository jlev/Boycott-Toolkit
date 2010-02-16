#from django.contrib.gis.db import models
from django.db import models

class Location(models.Model):
    name = models.CharField('Locality Name',max_length=100)
    address = models.TextField(max_length=100,null=True,blank=True)
    city = models.CharField(max_length=25,null=True,blank=True)
    state = models.CharField(max_length=25,null=True,blank=True)
    country = models.CharField(max_length=25,null=True,blank=True)
    #coordinates = models.PointField(srid=4326)
    radius = models.FloatField("Radius of specificity, in km",default=1)
    #objects = models.GeoManager()
    def __unicode__(self):
        return self.name