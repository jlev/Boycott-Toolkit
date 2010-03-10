from django import forms
from tagging.forms import TagField
from autocomplete.widgets import TagAutocomplete

from django.contrib import admin
from target.models import Product,Company,Campaign,ProductAction,CompanyAction
from reversion.admin import VersionAdmin

#ADMIN FORMS
class TrackedObjectAdminForm(forms.ModelForm):
    class Meta:
        pass

class CompanyAdminForm(TrackedObjectAdminForm):
    tags = TagField(widget=TagAutocomplete(), required=False)
    class Meta(TrackedObjectAdminForm.Meta):
        model = Company

class ProductAdminForm(TrackedObjectAdminForm):
    tags = TagField(widget=TagAutocomplete(), required=False)
    class Meta(TrackedObjectAdminForm.Meta):
        model = Product

class CampaignAdminForm(TrackedObjectAdminForm):
    tags = TagField(widget=TagAutocomplete(), required=False)
    class Meta(TrackedObjectAdminForm.Meta):
        model = Campaign

class TrackedAdmin(VersionAdmin):
    def save_model(self, request, obj, form, change):
        '''Override the save_model so that we can keep track of who edited the object in the admin.
        Views take care of this separately.'''
        if not change:
            #it's new
            obj.added_by = request.user
        obj.save() #create the object, so we have a primary key
        obj.edited_by.add(request.user)
        obj.save() #save again

class ProductAdmin(TrackedAdmin):
    form = ProductAdminForm
    
class CompanyAdmin(TrackedAdmin):
    form = CompanyAdminForm
    
class CampaignAdmin(TrackedAdmin):
    form = CampaignAdminForm

admin.site.register(Product,ProductAdmin)
admin.site.register(Company,CompanyAdmin)
admin.site.register(Campaign,CampaignAdmin)
admin.site.register(ProductAction)
admin.site.register(CompanyAction)