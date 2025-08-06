from django import forms

from .models import People


class SearchForm(forms.Form):
    # Dynamically create choices for the gender dropdown, ensuring no duplicates.
    GENDER_CHOICES = [("", "---------")] + [
        (gender, gender)
        for gender in People.objects.values_list("gender", flat=True)
        .distinct()
        .order_by("gender")
        if gender
    ]

    min_release_date = forms.DateField(
        label="Movies minimum release date", required=True
    )
    max_release_date = forms.DateField(
        label="Movies maximum release date", required=True
    )
    planet_diameter = forms.IntegerField(
        label="Planet diameter greater than", required=True
    )
    character_gender = forms.ChoiceField(
        choices=GENDER_CHOICES, label="Character gender", required=True
    )
