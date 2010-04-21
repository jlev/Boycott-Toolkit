from django import forms
from tagging.forms import TagField
from autocomplete.widgets import TagAutocomplete,Autocomplete
from info.widgets import CitationWidget
from target.models import Product,Company,Store,Campaign,ProductAction,CompanyAction

#MAIN FORMS FOR USER DISPLAY
class TrackedObjectForm(forms.ModelForm):
    class Meta:
        #hide the non-editable fields in the main form
        exclude=('added_by','edited_by','added_date','slug')

class CompanyForm(TrackedObjectForm):
    tags = TagField(widget=TagAutocomplete(), required=False)
    
    def __init__(self, *args, **kwargs):
        super(CompanyForm, self).__init__(*args, **kwargs)
        self.fields['description'] = forms.fields.CharField(widget=CitationWidget(attrs={'model':'target.company','field':'description'}))
        self.fields['citations_json'] = forms.fields.CharField(widget=forms.widgets.HiddenInput(),required=False) #holds all the citations as json
    class Meta(TrackedObjectForm.Meta):
        exclude = TrackedObjectForm.Meta.exclude + ('map',)
        model = Company
 
class ProductForm(TrackedObjectForm):
    tags = TagField(widget=TagAutocomplete(), required=False)  
    
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['description'] = forms.fields.CharField(widget=CitationWidget(attrs={'model':'target.product','field':'description'}))
        self.fields['citations_json'] = forms.fields.CharField(widget=forms.widgets.HiddenInput(),required=False) #holds all the citations as json 
    class Meta(TrackedObjectForm.Meta):
        model = Product

class StoreForm(TrackedObjectForm):
    tags = TagField(widget=TagAutocomplete(), required=False)
    class Meta(TrackedObjectForm.Meta):
        exclude = TrackedObjectForm.Meta.exclude + ('location',)
        model = Store
   
class CampaignForm(TrackedObjectForm):
    tags = TagField(widget=TagAutocomplete(), required=False)
    
    def __init__(self, *args, **kwargs):
           super(CampaignForm, self).__init__(*args, **kwargs)
           self.fields['description'] = forms.fields.CharField(widget=CitationWidget(attrs={'model':'target.campaign','field':'description'}))
           self.fields['criteria'] = forms.fields.CharField(label="Goal",help_text="When will this campaign be complete?",widget=CitationWidget(attrs={'model':'target.campaign','field':'criteria'}))
           self.fields['citations_json'] = forms.fields.CharField(widget=forms.widgets.HiddenInput(),required=False) #holds all the citations as json
           
    class Meta(TrackedObjectForm.Meta):
        exclude = TrackedObjectForm.Meta.exclude + ('highlight','companies','products')
        #highlight isn't user editable
        #companies and products are added after by the ProductAction and CompanyAction intermediates
        model = Campaign
   
#these are full action forms
class CompanyActionForm(forms.ModelForm):
    #company = TagField(widget=Autocomplete(attrs={'model':'target.Company'}))
    class Meta:
        model = CompanyAction
        
class ProductActionForm(forms.ModelForm):
    #product = TagField(widget=Autocomplete(attrs={'model':'target.Product'}))
    class Meta:
        model = ProductAction
        
#these are inline forms that are used when the parent company or product is added
class CompanyActionInlineForm(forms.ModelForm):
    reason = forms.fields.CharField(widget=forms.widgets.TextInput(),
                        help_text="One sentence reason why users should take this action.")
    class Meta:
        fields = ('campaign','verb','reason')
        model = CompanyAction
        
class ProductActionInlineForm(forms.ModelForm):
    reason = forms.fields.CharField(widget=forms.widgets.TextInput(),
                        help_text="One sentence reason why users should take this action.")
    class Meta:
        fields = ('campaign','verb','reason')
        model = ProductAction