from django import forms

from .models import People


class SearchForm(forms.Form):
    # On récupère les choix de genre, sans doublons, depuis la BDD
    GENDER_CHOICES = [
        (gender, gender.capitalize())
        for gender in People.objects.values_list("gender", flat=True).distinct()
    ]

    min_release_date = forms.DateField(
        label="Movies minimum release date",
        widget=forms.DateInput(attrs={"type": "date"}),
        required=True,
    )
    max_release_date = forms.DateField(
        label="Movies maximum release date",
        widget=forms.DateInput(attrs={"type": "date"}),
        required=True,
    )
    diameter_gt = forms.IntegerField(
        label="Planet diameter greater than", required=True
    )
    gender = forms.ChoiceField(
        label="Character gender", choices=GENDER_CHOICES, required=True
    )
