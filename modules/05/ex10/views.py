import json
import os

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render

from .forms import SearchForm
from .models import Movies, People, Planets


def search_view(request):
    form = SearchForm(request.GET or None)
    results = None

    if form.is_valid():
        # If the form is submitted and valid, filter the data.
        min_date = form.cleaned_data["min_release_date"]
        max_date = form.cleaned_data["max_release_date"]
        diameter = form.cleaned_data["planet_diameter"]
        gender = form.cleaned_data["character_gender"]

        # This is the complex ORM query that filters across all three models.
        results = (
            People.objects.filter(
                gender=gender,
                homeworld__diameter__gte=diameter,
                movies__release_date__range=(min_date, max_date),
            )
            .distinct()
            .select_related("homeworld")
        )
        # print(results)

    return render(request, "ex10/search.html", {"form": form, "results": results})


def populate(request):
    """
    Manually populates the database from the fixture file.
    It performs multiple passes and correctly handles null foreign keys.
    """
    # Clear existing data to make the view re-runnable
    Movies.objects.all().delete()
    People.objects.all().delete()
    Planets.objects.all().delete()

    fixture_path = os.path.join(settings.BASE_DIR, "ex10_initial_data.json")

    try:
        with open(fixture_path, "r") as f:
            data = json.load(f)

        # First pass: Create all Planet objects
        for item in data:
            if item["model"] == "ex10.planets":
                Planets.objects.create(pk=item["pk"], **item["fields"])

        # Second pass: Create all People objects
        for item in data:
            if item["model"] == "ex10.people":
                fields = item["fields"]
                homeworld_pk = fields.pop(
                    "homeworld", None
                )  # Use .pop with a default value

                # Check if a homeworld was specified for this person.
                if homeworld_pk is not None:
                    # If there is a homeworld, find the Planet instance and link it.
                    homeworld_instance = Planets.objects.get(pk=homeworld_pk)
                    People.objects.create(
                        pk=item["pk"], homeworld=homeworld_instance, **fields
                    )
                else:
                    # If homeworld is null, create the Person without a homeworld link.
                    People.objects.create(pk=item["pk"], homeworld=None, **fields)

        # Third pass: Create Movies and their M2M relationships
        for item in data:
            if item["model"] == "ex10.movies":
                # Remove fields that are not in the Movies model before creating the object
                if "characters" in item["fields"]:
                    character_pks = item["fields"].pop("characters")
                else:
                    character_pks = []

                movie = Movies.objects.create(pk=item["pk"], **item["fields"])

                # Set the many-to-many relationship after the movie is created
                if character_pks:
                    movie.characters.set(People.objects.filter(pk__in=character_pks))

        return HttpResponse("Data populated successfully.")

    except Exception as e:
        return HttpResponse(f"An unexpected error occurred: {e}")
