from django import forms

from .models import Movies


class UpdateForm(forms.Form):
    # This field creates a dropdown list from all Movie objects.
    # It will display the movie's title but return its primary key (episode_nb).
    movie = forms.ModelChoiceField(
        queryset=Movies.objects.all(), label="Select a Movie"
    )

    # This field creates a text area for the new opening crawl text.
    opening_crawl = forms.CharField(widget=forms.Textarea, label="New Opening Crawl")
