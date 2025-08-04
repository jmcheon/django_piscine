# dans ex05/views.py
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .models import Movies


def populate(request):
    """
    Peuple la base de données en utilisant la méthode ORM get_or_create.
    Cela réinsère les données supprimées comme demandé. [cite: 193]
    """
    movies_data = [
        {
            "episode_nb": 1,
            "title": "The Phantom Menace",
            "director": "George Lucas",
            "producer": "Rick McCallum",
            "release_date": "1999-05-19",
        },
        {
            "episode_nb": 2,
            "title": "Attack of the Clones",
            "director": "George Lucas",
            "producer": "Rick McCallum",
            "release_date": "2002-05-16",
        },
        # ... (ajoutez les autres films comme dans ex03)
        {
            "episode_nb": 7,
            "title": "The Force Awakens",
            "director": "J. J. Abrams",
            "producer": "Kathleen Kennedy, J. J. Abrams, Bryan Burk",
            "release_date": "2015-12-11",
        },
    ]

    results = []
    for data in movies_data:
        movie, created = Movies.objects.get_or_create(
            episode_nb=data["episode_nb"], defaults=data
        )
        if created:
            results.append(f"OK: {movie.title} inserted.")
        else:
            results.append(f"OK: {movie.title} already exists.")
    return HttpResponse("<br>".join(results))


def display(request):
    """Affiche les films en utilisant l'ORM."""
    movies = Movies.objects.all()
    if not movies:
        return HttpResponse("No data available")
    return render(request, "ex05/display.html", {"movies": movies})


def remove(request):
    """
    Affiche un formulaire pour supprimer un film et gère la suppression
    en utilisant l'ORM.
    """
    if request.method == "POST":
        # Récupère l'ID (clé primaire) du film à supprimer depuis le formulaire
        episode_nb_to_remove = request.POST.get("movie_episode_nb")
        if episode_nb_to_remove:
            try:
                # Utilise l'ORM pour trouver le film...
                movie_to_delete = Movies.objects.get(episode_nb=episode_nb_to_remove)
                # ...et le supprimer.
                movie_to_delete.delete()
            except Movies.DoesNotExist:
                # Gère le cas où le film n'existe pas (sécurité)
                pass
        # Redirige vers la même page pour réafficher le formulaire mis à jour
        return redirect("remove")

    # Pour une requête GET (premier affichage)
    movies = Movies.objects.all()
    if not movies:
        return HttpResponse("No data available")

    # Affiche le formulaire
    return render(request, "ex05/remove.html", {"movies": movies})
