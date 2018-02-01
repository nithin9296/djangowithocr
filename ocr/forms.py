from django import forms
from ocr.models import trialbalance2017

class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a File'
        )



class trialbalanceform(forms.Form):
    trialbalancefile = forms.FileField(
        label = 'Upload current year trialbalance'
        )
    

