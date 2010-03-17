from django.db import models
from django.contrib.auth.models import User
from django_stdimage import StdImageField
from target.models import Product,Company,Campaign
from facebookconnect.models import FacebookProfile

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    image = StdImageField(upload_to="uploads/users",blank=True,null=True,size=(400,400),thumbnail_size=(100,100))
    #TODO: connect FacebookProfile post_save signal to cache avatar image
    description = models.TextField(help_text="Tell us about yourself.",blank=True,null=True)
    campaigns = models.ManyToManyField(Campaign,related_name="users_joined_campaign",help_text="Campaigns I have joined",blank=True,null=True)
    
    
    @models.permalink
    def get_absolute_url(self):
        return ('community.views.user_view', [self.user.username])
        
    def __unicode__(self):
        return self.user.__unicode__()
        
    def get_num_fb_friends(self):
        '''Get the number of friends'''
        try:
            my_profile = FacebookProfile.objects.get(user=self.user)
            my_friends = my_profile._FacebookProfile__get_facebook_friends()
            return len(my_friends)
        except FacebookProfile.DoesNotExist:
            return None
        
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])