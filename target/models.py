from django.db import models
from django.contrib.auth.models import User
from django_stdimage import StdImageField
import tagging.fields
from tagging.utils import parse_tag_input

from geography.models import Map

class TargetBase(models.Model):
    name = models.CharField('Name',max_length=200)
    slug = models.SlugField('Slug',max_length=200,null=True)
    description = models.TextField(help_text='''Description field.<br><small>URLs and linebreaks will be converted to HTML.</small>''',blank=True,null=True)
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
    #TODO: connect post_save signal here to user log


class Company(TargetBase):
    logo = StdImageField(upload_to="uploads/logos",blank=True,size=(250,250),thumbnail_size=(150,75))
    address = models.TextField(max_length=100,null=True,blank=True)
    map = models.ForeignKey(Map,blank=True,null=True)
    website = models.URLField(blank=True,null=True)
    phone = models.CharField(max_length=15,blank=True,null=True) #validate?
    class Meta(TargetBase.Meta):
        verbose_name_plural = "Companies"
    @models.permalink
    def get_absolute_url(self):
        return ('target.views.company_view', [self.slug])

class Product(TargetBase):
    company = models.ForeignKey('Company',help_text="Who makes this product?")
    upc = models.CharField('UPC',max_length=13,blank=True,null=True)
    image = StdImageField(upload_to="uploads/products",blank=True,size=(250,250),thumbnail_size=(150,75))
    @models.permalink
    def get_absolute_url(self):
        return ('target.views.product_view', [self.slug])

COMPANY_VERB_CHOICES = (
    ('OPPOSE','Oppose'),
    ('SUPPORT','Support'),
)

class CompanyAction(models.Model):
    '''Intermediate model between a campaign and a company.
    Defines whether the relationship is negative (the default) or positive (the exception).
    So we can have campaigns that include both companies to boycott and alternatives to support.'''
    campaign = models.ForeignKey('Campaign')
    company = models.ForeignKey('Company')
    verb = models.CharField(choices=COMPANY_VERB_CHOICES,default="OPPOSE",max_length=10,
                        help_text="Are you asking users to support or oppose this company?")
    reason = models.TextField(blank=True,null=True,max_length=500,
                              help_text="One sentence reason why users should take this action.")
    class Meta:
        unique_together = ("campaign", "company")
    def __unicode__(self):
        return "%s:%s %s" % (self.campaign,self.get_verb_display(),self.company)
    def positive(self):
        if self.verb is 'SUPPORT':
            return True
        else:
            return False

PRODUCT_VERB_CHOICES = (
    ('BOYCOTT','Boycott'),
    ('BUY','Buy'),
)

class ProductAction(models.Model):
    '''Intermediate model between a campaign and a product.
    Defines whether the relationship is negative (the default) or positive (the exception).
    So we can have campaigns that include both products to boycott and alternatives to support.'''
    campaign = models.ForeignKey('Campaign')
    product = models.ForeignKey('Product')
    verb = models.CharField(choices=PRODUCT_VERB_CHOICES,default="BOYCOTT",max_length=10,
                            help_text="Are you asking users to buy or boycott this product?")
    reason = models.TextField(blank=True,null=True,max_length=500,
                              help_text="One sentence reason why users should take this action.")
    class Meta:
        unique_together = ("campaign", "product")
    def __unicode__(self):
        return "%s:%s %s" % (self.campaign,self.get_verb_display(),self.product)
    def positive(self):
        if self.verb is "BUY":
            return True
        else:
            return False

CAMPAIGN_VERB_CHOICES = (
    ('BOYCOTT','Boycott'),
    ('SUPPORT','Support'),
)

class Campaign(TargetBase):
    verb = models.CharField(choices=CAMPAIGN_VERB_CHOICES,default="BOYCOTT",max_length=10,
                            help_text="Is this a support or boycott campaign?")
    criteria = models.TextField(blank=True,null=True,help_text="When will this campaign be complete?")
    complete = models.BooleanField(default=False)
    companies = models.ManyToManyField('Company',through='CompanyAction')
    products =  models.ManyToManyField('Product',through='ProductAction')
    highlight = models.BooleanField(default=False, help_text="Highlight on the frontpage, and lets the top-level url resolve")
    @models.permalink
    def get_absolute_url(self):
        return ('target.views.campaign_view', [self.slug])
    