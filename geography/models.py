from django.db import models
import tagging.fields

class Location(models.Model):
    name = models.CharField('Locality Name',max_length=100)
    tags = tagging.fields.TagField()
    gt_url = models.URLField('GroundTruth URL',blank=True,null=True)
    embed_code = models.TextField('Mapping service embed code',blank=True,null=True)
    def __unicode__(self):
        return self.name
    def get_absolute_url(self):
        return "/location/%s",self.name
