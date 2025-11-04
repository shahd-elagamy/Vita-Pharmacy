from django import forms

class DnaUploadForm(forms.Form):
    dna_file = forms.FileField(label='Upload DNA CSV file')
