from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django_stdimage import StdImageField
import tagging.fields
from tagging.utils import parse_tag_input


class TargetBase(models.Model):
    name = models.CharField('Name',max_length=200)
    description = models.TextField(blank=True,null=True)
    tags = tagging.fields.TagField()
    
    #these are required, but need to be null=true so that they can pass validation
    #filled in TrackedAdmin.save_model and the related edit views
    #there should be a better way to do this...
    added_by = models.ForeignKey(User,related_name="%(class)s_add",null=True,blank=True)
    edited_by = models.ManyToManyField(User,related_name="%(class)s_edit",null=True,blank=True)
    added_date = models.DateTimeField(auto_now_add=True)
    def get_tag_list(self):
        return parse_tag_input(self.tags)
    class Meta:
        abstract=True


class Company(TargetBase):
    logo = StdImageField(upload_to="uploads/logos",blank=True,size=(400,400),thumbnail_size=(150,120))
    location = models.ForeignKey('geography.Location',blank=True,null=True)
    website = models.URLField(blank=True,null=True)
    phone = models.CharField(max_length=15,blank=True,null=True) #validate?
    class Meta(TargetBase.Meta):
        verbose_name_plural = "Companies"
    def __unicode__(self):
        return self.name
        
    @models.permalink
    def get_absolute_url(self):
        return ('target.views.company_view', [slugify(self.name)])

class Product(TargetBase):
    company = models.ForeignKey('Company')
    upc = models.CharField('UPC',max_length=13,blank=True,null=True)
    image = StdImageField(upload_to="uploads/products",blank=True,size=(400,400),thumbnail_size=(150,120))
    def __unicode__(self):
        return self.name
    @models.permalink
    def get_absolute_url(self):
        return ('target.views.product_view', [slugify(self.name)])
        
class Campaign(TargetBase):
    started_by = models.ForeignKey(User)
    criteria = models.TextField(blank=True,null=True)
    complete = models.BooleanField(default=False)
    companies = models.ManyToManyField(Company)
    products =  models.ManyToManyField(Product)