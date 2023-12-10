from django import forms
from classes.models import Class
# from django.contrib.auth.models import User
import re

class NextClassForm(forms.ModelForm):
    class Meta:
        model=Class 
        fields = ['classname','semester','excel_file','session']
        widgets = {
            'classname': forms.TextInput(attrs={'placeholder': 'class+year e.g. fymca2023'}),
            'semester': forms.TextInput(attrs={'placeholder': 'Select semester'}),
            # 'semester':forms.ChoiceField(choices=[(i, i) for i in range(1, 5)]),
            'excel_file': forms.FileInput(attrs={'placeholder': 'Choose Excel file'}),
            'session': forms.Select(attrs={'placeholder': 'Select session'}),
        }

    def clean_classname(self):
        classname = self.cleaned_data.get('classname')
        pattern = re.compile(r'^(fymca|symca)\d{4}$')
        if not pattern.match(classname):
            raise forms.ValidationError('Invalid class name format. Please use "fymca" or "symca" followed by a 4-digit year.')
        return classname