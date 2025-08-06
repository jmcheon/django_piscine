from django.http import HttpResponse

from .models import Movies


def populate(request):
    """
    Insère les données des films en utilisant l'ORM.
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
            "producer": "Gary Kutz, Rick McCallum",
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
    for movie_data in movies_data:
        try:
            # get_or_create tente de récupérer l'objet, et le crée s'il n'existe pas.
            # 'created' est un booléen qui indique si un nouvel objet a été créé.
            obj, created = Movies.objects.get_or_create(**movie_data)
            if created:
                results.append(f"OK: {obj.title} inserted.")
            else:
                results.append(f"Error: {obj.title} already exists.")
        except Exception as e:
            results.append(f"Error inserting {movie_data['title']}: {e}")

    return HttpResponse("<br>".join(results))


def display(request):
    """
    Displays the data using the ORM
    """
    try:
        # Retrieve all Movie objects from the database.
        movies = Movies.objects.all()

        if not movies:
            return HttpResponse("No data available")

        # Create an HTML table to display the data.
        html = "<table border='1'>"

        html += "<tr><th>Episode Nb</th><th>Title</th><th>Opening Crawl</th><th>Director</th><th>Producer</th><th>Release Date</th></tr>"

        for movie in movies:
            html += "<tr>"

            html += f"<td>{movie.episode_nb}</td>"
            html += f"<td>{movie.title}</td>"

            opening_crawl_text = (
                movie.opening_crawl if movie.opening_crawl is not None else "N/A"
            )
            html += f"<td>{opening_crawl_text}</td>"

            html += f"<td>{movie.director}</td>"
            html += f"<td>{movie.producer}</td>"
            html += f"<td>{movie.release_date}</td>"
            html += "</tr>"

        html += "</table>"

        return HttpResponse(html)

    except Exception:
        return HttpResponse("No data available")
