from django import forms
from .models import TempRecipe


class SearchForm(forms.Form):
    SORT_CHOICES = [('1','Best Match'),('2','Newest'),('3','Popular')]
    search_keywords = forms.CharField(label='Enter ingredients', max_length = 200,
            widget=forms.TextInput(attrs={"placeholder":"chicken tacos keto etc..",}))
    sort_method = forms.ChoiceField(widget=forms.RadioSelect, choices=SORT_CHOICES)

class AddRecipeForm(forms.ModelForm):
    
    class Meta:
        model = TempRecipe
        fields = ["selected"]
        labels = {"selected": "add to list"}

    



    