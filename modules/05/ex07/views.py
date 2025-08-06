from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import UpdateForm
from .models import Movies


def populate(request):
    # This will populate the new table.
    # Note that we don't need to provide 'created' or 'updated' values.
    # Django handles them automatically thanks to auto_now_add and auto_now.
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
        {
            "episode_nb": 3,
            "title": "Revenge of the Sith",
            "director": "George Lucas",
            "producer": "Rick McCallum",
            "release_date": "2005-05-19",
        },
        {
            "episode_nb": 4,
            "title": "A New Hope",
            "director": "George Lucas",
            "producer": "Gary Kurtz, Rick McCallum",
            "release_date": "1977-05-25",
        },
        {
            "episode_nb": 5,
            "title": "The Empire Strikes Back",
            "director": "Irvin Kershner",
            "producer": "Gary Kurtz, Rick McCallum",
            "release_date": "1980-05-17",
        },
        {
            "episode_nb": 6,
            "title": "Return of the Jedi",
            "director": "Richard Marquand",
            "producer": "Howard G. Kazanjian, George Lucas, Rick McCallum",
            "release_date": "1983-05-25",
        },
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
        Movies.objects.get_or_create(episode_nb=data["episode_nb"], defaults=data)
        results.append("OK<br>")
    return HttpResponse("".join(results))


def display(request):
    movies = Movies.objects.all()
    if not movies:
        return HttpResponse("No data available")
    return render(request, "ex07/display.html", {"movies": movies})


def update(request):
    if request.method == "POST":
        # Create a form instance and populate it with data from the request.
        form = UpdateForm(request.POST)
        # Check if the form is valid.
        if form.is_valid():
            # Process the data in form.cleaned_data.
            movie_to_update = form.cleaned_data["movie"]
            new_crawl = form.cleaned_data["opening_crawl"]

            # Update the field.
            movie_to_update.opening_crawl = new_crawl
            # Save the object. This will automatically update the 'updated' field.
            movie_to_update.save()

            # Redirect to the same page to prevent form re-submission.
            return redirect("update")
    else:
        # If a GET (or any other method), create a blank form.
        form = UpdateForm()

    return render(request, "ex07/update.html", {"form": form})
