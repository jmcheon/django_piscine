from django import forms

from .models import People


class SearchForm(forms.Form):
    # Define the fields first without the dynamic choices.
    min_release_date = forms.DateField(
        label="Movies minimum release date", required=True
    )
    max_release_date = forms.DateField(
        label="Movies maximum release date", required=True
    )
    planet_diameter = forms.IntegerField(
        label="Planet diameter greater than", required=True
    )
    character_gender = forms.ChoiceField(label="Character gender", required=True)

    def __init__(self, *args, **kwargs):
        # This method runs when an instance of the form is created (e.g., in a view).
        # It does NOT run when 'migrate' is starting up.
        super().__init__(*args, **kwargs)

        # We build the choices here, safely at runtime.
        try:
            gender_choices = [
                (g, g)
                for g in People.objects.values_list("gender", flat=True)
                .distinct()
                .order_by("gender")
                if g
            ]
            self.fields["character_gender"].choices = [
                ("", "---------")
            ] + gender_choices
        except Exception:
            # If the table doesn't exist yet (e.g., during the very first migrate),
            # this prevents a crash and provides an empty choice list.
            self.fields["character_gender"].choices = [("", "---------")]
