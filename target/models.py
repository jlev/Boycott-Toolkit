from django.db import models
from django.contrib.gis.db import models as gis_models
from django.contrib.auth.models import User
from stdimage import StdImageField
import tagging.fields
from tagging.utils import parse_tag_input

from geography.models import Map

class TargetBase(models.Model):
    name = models.CharField('Name',max_length=200)
    slug = models.SlugField('Slug',max_length=200,null=True)
    description = models.TextField(help_text='''URLs and linebreaks will be converted to HTML.''',blank=True,null=True)
    tags = tagging.fields.TagField()
    #public = models.BooleanField(help_text="Should this be viewable to all users?",default=False)
    #defaults to false, but reset to True after form validation
    
    #these are required, but need to be null=true so that they can pass validation
    #filled in TrackedAdmin.save_model and the related edit views
    added_by = models.ForeignKey(User,related_name="%(class)s_add",null=True)
    edited_by = models.ManyToManyField(User,related_name="%(class)s_edit",null=True)
    added_date = models.DateTimeField(auto_now_add=True)
    def get_tag_list(self):
        return parse_tag_input(self.tags)
    def __unicode__(self):
        return self.name
    class Meta:
        abstract=True
        ordering = ('name',)

class Company(TargetBase):
    logo = StdImageField("Company Logo",upload_to="uploads/logos",blank=True,size=(250,250),thumbnail_size=(150,75))
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
    upc_image = models.ImageField('UPC Image',upload_to='uploads/products/upc',blank=True,null=True)
    image = StdImageField("Product Image",upload_to="uploads/products",blank=True,size=(250,250),thumbnail_size=(150,75))
    alternative = models.ForeignKey('Product',help_text="What products make a good alternative?",blank=True,null=True)
    @models.permalink
    def get_absolute_url(self):
        return ('target.views.product_view', [self.slug])
        
    def generate_barcode(self):
        "generates barcode png and returns filename"
        try:
            import barcode
        except ImportError:
            #not installed
            return None
        
        if not self.upc:
            return None
        EAN = barcode.get_barcode_class('ean13')
        upc_filename = EAN(self.upc, writer=barcode.writer.ImageWriter()).save('%s.png' % self.upc)
        return upc_filename
    
    def save(self, *args, **kwargs):
        if self.upc and not self.upc_image:
            self.upc_image = self.generate_barcode()
        super(Product, self).save(*args, **kwargs)

class Store(TargetBase):
    logo = StdImageField("Store Logo",upload_to="uploads/store",blank=True,null=True,size=(250,250),thumbnail_size=(150,75))
    address = models.TextField(max_length=100,null=True,blank=True)
    location = gis_models.PointField(srid=4326,blank=True,null=True)
    phone = models.CharField(max_length=15,blank=True,null=True)
    website = models.URLField(blank=True,null=True)
    products = models.ManyToManyField('Product',help_text="Products that this store sells")
    @models.permalink
    def get_absolute_url(self):
        return ('target.views.store_view', [self.slug])

COMPANY_VERB_CHOICES = (
    ('OPPOSE','Oppose'),
    ('SUPPORT','Support'),
)

class CompanyAction(models.Model):
    '''Intermediate model between a campaign and a company.
    Defines whether the relationship is negative (the default) or positive (the exception).
    So we can have campaigns that include both companies to boycott and alternatives to support.'''
    campaign = models.ForeignKey('Campaign')
    company = models.ForeignKey('Company',null=True) #null so the inline form can create, then add fk later
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
    product = models.ForeignKey('Product',null=True) #null so the inline form can create, then add fk later
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
    ('SUPPORT','Support')
)

class Campaign(TargetBase):
    verb = models.CharField(choices=CAMPAIGN_VERB_CHOICES,default="BOYCOTT",max_length=10,
                            help_text="Is this a support or boycott campaign?")
    criteria = models.TextField("Goal",blank=True,null=True,help_text="When will this campaign be complete?")
    complete = models.BooleanField(default=False,help_text="Have the goals been satisfied?")
    companies = models.ManyToManyField('Company',through='CompanyAction')
    products =  models.ManyToManyField('Product',through='ProductAction')
    highlight = models.BooleanField(default=False, help_text="Highlight on the frontpage, and lets the top-level url resolve")
    graveyard = models.BooleanField(default=False, help_text="Remove for TOS violation")
    extra = models.TextField("Extra HTML Field",blank=True,null=True)
    @models.permalink
    def get_absolute_url(self):
        return ('target.views.campaign_view', [self.slug])
    def positive(self):
        if (self.verb == "SUPPORT"):
            return True
        else:
            return False
    
