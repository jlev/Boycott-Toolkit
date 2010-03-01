from django import forms
#from autocomplete.widgets import Autocomplete,DynamicAutocomplete
from info.models import Citation,Source

class CitationForm(forms.ModelForm):
    #source = forms.ModelChoiceField(Source._default_manager.get_query_set())
    #cited_type = forms.ChoiceField(widget=DynamicAutocomplete(attrs={'type':'list','model':'OVERWRITE'}))
    #cited_field = forms.ChoiceField(widget=DynamicAutocomplete(attrs={'type':'fields','search_name':'cited_field'}))
    #cited_id = forms.CharField(initial=0,widget=forms.widgets.HiddenInput())
    #cited_name = forms.ChoiceField(widget=DynamicAutocomplete(attrs={'type':'list','search_name':'cited_type'}))
    
    class Meta:
        model = Citation