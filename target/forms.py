from django import forms
from django.db.models import get_model
from tagging.forms import TagField
from autocomplete.widgets import TagAutocomplete
from target.models import Product,Company,Campaign

class TrackedObjectForm(forms.ModelForm):
    class Meta:
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
    exclude = ('highlight')
    class Meta(TrackedObjectForm.Meta):
        model = Campaign
        