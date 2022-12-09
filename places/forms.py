from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Review, Place#, ACCESS_CHOICES
from django.conf import settings

class AdvancedSearchForm1(forms.Form):
    location = forms.MultipleChoiceField(
        choices=Place.LOCATION_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple(
            attrs={'class': "search-form-checkbox"}
        ),
        localize=True
        )

class AdvancedSearchForm2(forms.Form):
    type = forms.MultipleChoiceField(
        choices=Place.TYPE_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple(
            attrs={'class': "search-form-checkbox"}
        ),
        localize=True
        )

class AdvancedSearchForm3(forms.Form):
    access = forms.MultipleChoiceField(
        choices=Review.SCORE_CATEGORY_CHOICES,
        required=False,
        widget=forms.RadioSelect(
            attrs={'class': "search-form-checkbox"}
        ),
        localize=True
        )

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review 
        fields = [ i[0] for i in model.SCORE_CATEGORY_CHOICES]
        localized_fields = '__all__'
        # required_fields = 
        widgets = {f: forms.RadioSelect(
            attrs={
                'class': "radio-field",
            },
        ) for f in fields}