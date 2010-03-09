from django import forms
from django.db.models import get_model
from tagging.forms import TagField
from autocomplete.widgets import TagAutocomplete
from target.models import Product,Company,Campaign

#MAIN FORMS FOR USER DISPLAY
class TrackedObjectForm(forms.ModelForm):
    class Meta:
        #hide the non-editable fields in the main form
        exclude=('added_by','edited_by','added_date','slug')

class CompanyForm(TrackedObjectForm):
    tags = TagField(widget=TagAutocomplete(), required=False)
    class Meta(TrackedObjectForm.Meta):
        model = Company
 
class ProductForm(TrackedObjectForm):
    tags = TagField(widget=TagAutocomplete(), required=False)
    class Meta(TrackedObjectForm.Meta):
        model = Product
       
class CampaignForm(TrackedObjectForm):
    tags = TagField(widget=TagAutocomplete(), required=False)
    class Meta(TrackedObjectForm.Meta):
        exclude = TrackedObjectForm.Meta.exclude + ('highlight','companies','products')
        #highlight isn't user editable
        #companies and products are added after by the ProductAction and CompanyAction intermediates
        model = Campaign
   
#ADMIN FORMS
class TrackedObjectAdminForm(forms.ModelForm):
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