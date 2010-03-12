from django.db import models
from django.contrib.auth.models import User
from target.models import Product,Company,Campaign
from django_stdimage import StdImageField

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    image = StdImageField(upload_to="uploads/users",blank=True,size=(400,400),thumbnail_size=(100,100))
    description = models.CharField(max_length=50)
    campaigns = models.ManyToManyField(Campaign,related_name="users_joined_campaign",help_text="Campaigns I have joined",blank=True,null=True)
    
    @models.permalink
    def get_absolute_url(self):
        return ('community.views.user_view', [self.user.username])
        
    def __unicode__(self):
        return self.user.__unicode__()
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])