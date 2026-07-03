from django import forms
from .symptoms import SYMPTOMS

class SymptomForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for symptom in SYMPTOMS:
            self.fields[symptom] = forms.BooleanField(
                required=False,
                label=symptom.replace('_', ' ').title()
            )
