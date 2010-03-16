from django.contrib.gis.db import models
import tagging.fields

class Map(models.Model):
    name = models.CharField('City',max_length=100)
    #tags = tagging.fields.TagField()
    center = models.PointField(srid=4326)
    zoom = models.PositiveSmallIntegerField()
    area_info = models.ForeignKey('AreaInfo',blank=True,null=True,help_text="Add extra map layers for a specific region.")
    #markers = models.MultiPointField(srid=4326,blank=True,null=True)
    objects = models.GeoManager()
    def __unicode__(self):
        return self.name
    def get_absolute_url(self):
        return "/location/%s" % self.id

class AreaInfo(models.Model):
    name = models.CharField(max_length=50)
    script = models.TextField("OpenLayers javascript")
    def __unicode__(self):
        return self.name