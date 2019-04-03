from django import forms
from .models import CategorySite


class CategorySiteForm(forms.Form):
    select_category = forms.ModelChoiceField(queryset=CategorySite.objects.all())

    def save(self):
        print(self)