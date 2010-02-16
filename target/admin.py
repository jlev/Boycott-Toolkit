from django.contrib import admin
from target.models import Product,Company,Campaign
from target.forms import ProductForm,CompanyForm,CampaignForm
from reversion.admin import VersionAdmin

class TrackedAdmin(VersionAdmin):
    def save_model(self, request, obj, form, change):
        print form
        if not change:
            #it's new
            obj.added_by = request.user
        obj.save() #create the object, so we have a primary key
        obj.edited_by.add(request.user)
        obj.save() #save again

class ProductAdmin(TrackedAdmin):
    form = ProductForm
    
class CompanyAdmin(TrackedAdmin):
    form = CompanyForm
    
class CampaignAdmin(TrackedAdmin):
    form = CampaignForm
    
admin.site.register(Product,ProductAdmin)
admin.site.register(Company,CompanyAdmin)
admin.site.register(Campaign,CampaignAdmin)