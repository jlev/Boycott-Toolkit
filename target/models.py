from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django_stdimage import StdImageField
import tagging.fields
from tagging.utils import parse_tag_input

from geography.models import Location

class TargetBase(models.Model):
    name = models.CharField('Name',max_length=200)
    slug = models.CharField('Slug',max_length=200,null=True)
    description = models.TextField(help_text='''Can contain formatting in
        <a href=http://en.wikipedia.org/wiki/Markdown#Syntax_examples target=_blank>Markdown syntax</a>''',blank=True,null=True)
    tags = tagging.fields.TagField()
    
    #these are required, but need to be null=true so that they can pass validation
    #filled in TrackedAdmin.save_model and the related edit views
    added_by = models.ForeignKey(User,related_name="%(class)s_add",null=True,blank=True)
    edited_by = models.ManyToManyField(User,related_name="%(class)s_edit",null=True,blank=True)
    added_date = models.DateTimeField(auto_now_add=True)
    def get_tag_list(self):
        return parse_tag_input(self.tags)
    def __unicode__(self):
        return self.name
    class Meta:
        abstract=True


class Company(TargetBase):
    logo = StdImageField(upload_to="uploads/logos",blank=True,size=(250,250),thumbnail_size=(150,75))
    location = models.ForeignKey(Location,blank=True,null=True)
    website = models.URLField(blank=True,null=True)
    phone = models.CharField(max_length=15,blank=True,null=True) #validate?
    class Meta(TargetBase.Meta):
        verbose_name_plural = "Companies"
    @models.permalink
    def get_absolute_url(self):
        return ('target.views.company_view', [slugify(self.name)])

class Product(TargetBase):
    company = models.ForeignKey('Company')
    upc = models.CharField('UPC',max_length=13,blank=True,null=True)
    image = StdImageField(upload_to="uploads/products",blank=True,size=(250,250),thumbnail_size=(150,75))
    @models.permalink
    def get_absolute_url(self):
        return ('target.views.product_view', [slugify(self.name)])
        
class Campaign(TargetBase):
    criteria = models.TextField(blank=True,null=True)
    complete = models.BooleanField(default=False)
    companies = models.ManyToManyField(Company)
    products =  models.ManyToManyField(Product)
    highlight = models.BooleanField(default=False, help_text="Highlight on the frontpage, and lets the top-level url resolve")
    @models.permalink
    def get_absolute_url(self):
        return ('target.views.campaign_view', [slugify(self.name)])