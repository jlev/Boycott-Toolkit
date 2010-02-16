from django.contrib import admin
from community.models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(UserProfile,UserProfileAdmin)