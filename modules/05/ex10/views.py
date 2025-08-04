from django.shortcuts import render

from .forms import SearchForm
from .models import Movies


def search_view(request):
    form = SearchForm(request.POST or None)
    results = []

    if request.method == "POST" and form.is_valid():
        data = form.cleaned_data

        # On filtre les films selon les critères du formulaire
        # La magie de l'ORM permet de filtrer sur des modèles liés.
        movies = (
            Movies.objects.filter(
                release_date__gte=data["min_release_date"],
                release_date__lte=data["max_release_date"],
                characters__gender=data["gender"],
                characters__homeworld__diameter__gt=data["diameter_gt"],
            )
            .distinct()
            .prefetch_related("characters__homeworld")
        )

        # On prépare les résultats pour un affichage simple dans le template
        for movie in movies:
            for character in movie.characters.filter(
                gender=data["gender"], homeworld__diameter__gt=data["diameter_gt"]
            ):
                results.append(
                    {
                        "movie_title": movie.title,
                        "character_name": character.name,
                        "character_gender": character.gender,
                        "planet_name": character.homeworld.name,
                        "planet_diameter": character.homeworld.diameter,
                    }
                )

    context = {"form": form, "results": results}
    return render(request, "ex10/search.html", context)
