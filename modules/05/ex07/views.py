from django.http import HttpResponse
from django.shortcuts import redirect, render

from .models import Movies


def populate(request):
    """Peuple la table avec les données initiales."""
    movies_data = [
        # Collez la liste complète des films ici
        {
            "episode_nb": 1,
            "title": "The Phantom Menace",
            "director": "George Lucas",
            "producer": "Rick McCallum",
            "release_date": "1999-05-19",
            "opening_crawl": "",
        },
        {
            "episode_nb": 2,
            "title": "Attack of the Clones",
            "director": "George Lucas",
            "producer": "Rick McCallum",
            "release_date": "2002-05-16",
            "opening_crawl": "",
        },
        {
            "episode_nb": 3,
            "title": "Revenge of the Sith",
            "director": "George Lucas",
            "producer": "Rick McCallum",
            "release_date": "2005-05-19",
            "opening_crawl": "",
        },
        {
            "episode_nb": 4,
            "title": "A New Hope",
            "director": "George Lucas",
            "producer": "Gary Kurtz, Rick McCallum",
            "release_date": "1977-05-25",
            "opening_crawl": "",
        },
        {
            "episode_nb": 5,
            "title": "The Empire Strikes Back",
            "director": "Irvin Kershner",
            "producer": "Gary Kutz, Rick McCallum",
            "release_date": "1980-05-17",
            "opening_crawl": "",
        },
        {
            "episode_nb": 6,
            "title": "Return of the Jedi",
            "director": "Richard Marquand",
            "producer": "Howard G. Kazanjian, George Lucas, Rick McCallum",
            "release_date": "1983-05-25",
            "opening_crawl": "",
        },
        {
            "episode_nb": 7,
            "title": "The Force Awakens",
            "director": "J. J. Abrams",
            "producer": "Kathleen Kennedy, J. J. Abrams, Bryan Burk",
            "release_date": "2015-12-11",
            "opening_crawl": "",
        },
    ]
    results = []
    for data in movies_data:
        # get_or_create s'occupe de tout. Les champs created/updated sont gérés par le modèle.
        movie, created = Movies.objects.get_or_create(
            episode_nb=data["episode_nb"], defaults=data
        )
        if created:
            results.append(f"OK: {movie.title} inserted.")
        else:
            results.append(f"OK: {movie.title} already exists.")
    return HttpResponse("<br>".join(results))


def display(request):
    """Affiche tous les films de la base de données."""
    movies = Movies.objects.all()
    if not movies.exists():
        return HttpResponse("No data available")
    return render(request, "ex07/display.html", {"movies": movies})


def update(request):
    """Gère le formulaire de mise à jour du 'opening_crawl'."""
    if request.method == "POST":
        episode_nb = request.POST.get("movie_episode_nb")
        new_crawl = request.POST.get("opening_crawl")

        try:
            # On récupère le film à modifier
            movie_to_update = Movies.objects.get(episode_nb=episode_nb)
            # On modifie le champ
            movie_to_update.opening_crawl = new_crawl
            # On sauvegarde. C'est ici que le champ 'updated' est automatiquement mis à jour.
            movie_to_update.save()
        except Movies.DoesNotExist:
            return HttpResponse("Error: Movie not found.")
        # On redirige pour éviter le re-post du formulaire si l'utilisateur rafraîchit
        return redirect("update")

    # Si la méthode est GET, on affiche le formulaire
    movies = Movies.objects.all()
    if not movies.exists():
        return HttpResponse("No data available")
    return render(request, "ex07/update.html", {"movies": movies})
