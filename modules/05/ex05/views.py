# dans ex05/views.py
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Movies


# This function generates the full HTML page structure.
# It takes a title and the main content as arguments.
def render_full_html_page(page_title: str, content: str) -> str:
    """
    wraps the given content in a full, valid html5 document structure.
    """
    return f"""
    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <title>{page_title}</title>
    </head>
    <body>
        <h1>{page_title}</h1>
        <hr>
        {content}
    </body>
    </html>
    """


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
    try:
        if not Movies.objects.exists():
            pass
    except Exception as e:
        full_page = render_full_html_page("", "Error: Could not connect to the database.")
        return HttpResponse(full_page)


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
    """
    Displays movies using the ORM and the helper function for the HTML structure.
    """
    try:
        movies = Movies.objects.all()
        if not movies:
            content = "No data available"
        else:
            # First, build only the unique content for this view (the table).
            table_html = "<table border='1'>"
            table_html += "<tr><th>Episode Nb</th><th>Title</th><th>Opening Crawl</th><th>Director</th><th>Producer</th><th>Release Date</th></tr>"
            for movie in movies:
                table_html += "<tr>"
                table_html += f"<td>{movie.episode_nb}</td>"
                table_html += f"<td>{movie.title}</td>"
                opening_crawl_text = (
                    movie.opening_crawl if movie.opening_crawl is not None else "N/A"
                )
                table_html += f"<td>{opening_crawl_text}</td>"
                table_html += f"<td>{movie.director}</td>"
                table_html += f"<td>{movie.producer}</td>"
                table_html += f"<td>{movie.release_date}</td>"
                table_html += "</tr>"
            table_html += "</table>"
            content = table_html

        # Then, use the helper to wrap it in a full page.
        full_page = render_full_html_page("Movies List (ex05)", content)
        return HttpResponse(full_page)
    except Exception as e:
        full_page = render_full_html_page("", "No data available")
        # full_page = render_full_html_page("Error", f"An error occurred: {e}")
        return HttpResponse(full_page)


@csrf_exempt
def remove(request):
    """
    Handles movie removal and displays the form using the helper function.
    """
    try:
        if request.method == "POST":
            episode_nb_to_remove = request.POST.get("episode_nb")
            if episode_nb_to_remove:
                try:
                    movie_to_delete = Movies.objects.get(pk=episode_nb_to_remove)
                    movie_to_delete.delete()
                except Movies.DoesNotExist:
                    pass

        movies = Movies.objects.all()
        if not movies:
            content = "No data available"
        else:
            # Build only the unique content for this view (the form).
            form_html = "<form method='post'>"
            form_html += "<select name='episode_nb'>"
            for movie in movies:
                form_html += (
                    f"<option value='{movie.episode_nb}'>{movie.title}</option>"
                )
            form_html += "</select>"
            form_html += "<button type='submit' name='remove'>Remove</button>"
            form_html += "</form>"
            content = form_html

        # Use the helper to wrap it in a full page.
        full_page = render_full_html_page("Remove a Movie (ex05)", content)
        return HttpResponse(full_page)
    except Exception as e:
        full_page = render_full_html_page("", "No data available")
        # full_page = render_full_html_page("Error", f"An error occurred: {e}")
        return HttpResponse(full_page)
