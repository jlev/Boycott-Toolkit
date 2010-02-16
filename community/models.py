from django.db import models
from django.contrib.auth.models import User
from target.models import Product,Company
from django_stdimage import StdImageField

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    image = StdImageField(upload_to="uploads/users",blank=True,size=(400,400),thumbnail_size=(100,100))
    description = models.CharField(max_length=50)
    location = models.ForeignKey('geography.Location',null=True,blank=True)
    buy = models.ManyToManyField(Product,related_name="buy",help_text="Products I buy",blank=True,null=True)
    dontbuy = models.ManyToManyField(Product,related_name="dontbuy",help_text="Products I don't buy",blank=True,null=True)
    supports = models.ManyToManyField(Company,related_name="supports",help_text="Companies I support",blank=True,null=True)
    opposes = models.ManyToManyField(Company,related_name="opposes",help_text="Companies I oppose",blank=True,null=True)
    @models.permalink
    def get_absolute_url(self):
        return ('community.views.user_view', [self.user.username])
        
    def __unicode__(self):
        return self.user.__unicode__()
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])