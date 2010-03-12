from django import forms
from tagging.forms import TagField
from autocomplete.widgets import TagAutocomplete,Autocomplete
from target.models import Product,Company,Campaign,ProductAction,CompanyAction

#MAIN FORMS FOR USER DISPLAY
class TrackedObjectForm(forms.ModelForm):
    class Meta:
        #hide the non-editable fields in the main form
        exclude=('added_by','edited_by','added_date','slug')

class CompanyForm(TrackedObjectForm):
    tags = TagField(widget=TagAutocomplete(), required=False)
    class Meta(TrackedObjectForm.Meta):
        exclude = TrackedObjectForm.Meta.exclude + ('map',)
        model = Company
 
class ProductForm(TrackedObjectForm):
    tags = TagField(widget=TagAutocomplete(), required=False)
#    company = TagField(widget=Autocomplete(attrs={'model':'target.Company'}))
#    def clean_company(self):
#        name = self.cleaned_data['company']
#        the_company = Company.objects.get(name=name)
#        self.company = the_company
#        return self.cleaned_data       
    class Meta(TrackedObjectForm.Meta):
        model = Product
       
class CampaignForm(TrackedObjectForm):
    tags = TagField(widget=TagAutocomplete(), required=False)
    #TODO: fill in slug after form save
    class Meta(TrackedObjectForm.Meta):
        exclude = TrackedObjectForm.Meta.exclude + ('highlight','companies','products')
        #highlight isn't user editable
        #companies and products are added after by the ProductAction and CompanyAction intermediates
        model = Campaign
   
#these are full action forms
class CompanyActionForm(forms.ModelForm):
    company = TagField(widget=Autocomplete(attrs={'model':'target.Company'}))
    class Meta:
        model = CompanyAction
        
class ProductActionForm(forms.ModelForm):
    product = TagField(widget=Autocomplete(attrs={'model':'target.Product'}))
    class Meta:
        model = ProductAction
        
#these are inline forms that are used when the parent company or product is added
class CompanyActionInlineForm(forms.ModelForm):
    reason = forms.fields.CharField(widget=forms.widgets.TextInput(attrs={'size':'50'}),
                        help_text="One sentence reason why users should take this action.")
    class Meta:
        fields = ('campaign','verb','reason')
        model = CompanyAction
        
class ProductActionInlineForm(forms.ModelForm):
    reason = forms.fields.CharField(widget=forms.widgets.TextInput(attrs={'size':'50'}),
                        help_text="One sentence reason why users should take this action.")
    class Meta:
        fields = ('campaign','verb','reason')
        model = ProductAction