import psycopg2
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


def get_connection():
    """This function helps avoid repeating connection details."""
    try:
        return psycopg2.connect(
            dbname="formationdjango",
            user="djangouser",
            password="secret",
            host="localhost",
            port="5432",
        )
    except psycopg2.OperationalError:
        return None


def init(request):
    """This view creates the table for this exercise."""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS ex04_movies (
                    episode_nb  INT PRIMARY KEY,
                    title       VARCHAR(64) UNIQUE NOT NULL,
                    opening_crawl TEXT,
                    director    VARCHAR(32) NOT NULL,
                    producer    VARCHAR(128) NOT NULL,
                    release_date DATE NOT NULL
                );
                """)
        return HttpResponse("OK")
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}")


# This function generates the full HTML page structure.
# It takes a title and the main content as arguments.
def render_full_html_page(page_title: str, content: str) -> str:
    """
    Wraps the given content in a full, valid HTML5 document structure.
    """
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
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
    Peuple la table. La clause ON CONFLICT garantit que les données
    supprimées peuvent être réinsérées sans erreur.
    """
    # Ce code est identique à celui de l'ex02.
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
    conn = get_connection()
    if not conn:
        return HttpResponse("Error: Could not connect to the database.")
    results = []
    try:
        with conn.cursor() as cursor:
            for movie in movies_data:
                cursor.execute(
                    """
                    INSERT INTO ex04_movies (episode_nb, title, director, producer, release_date)
                    VALUES (%(episode_nb)s, %(title)s, %(director)s, %(producer)s, %(release_date)s)
                    ON CONFLICT (episode_nb) DO NOTHING;
                """,
                    movie,
                )
                if cursor.rowcount > 0:
                    results.append(f"OK: {movie['title']} inserted.")
                else:
                    results.append(f"OK: {movie['title']} already exists.")
        conn.commit()
        return HttpResponse("<br>".join(results))
    except Exception as e:
        return HttpResponse(f"An unexpected error occurred: {e}")
    finally:
        conn.close()


def display(request):
    """
    Displays data by building the content and passing it to the HTML page helper.
    """
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM ex04_movies;")
                movies = cursor.fetchall()

                if not movies:
                    content = "No data available"
                else:
                    # Build the unique content (the table).
                    table_content = "<table border='1'><tr>"
                    headers = [desc[0] for desc in cursor.description]
                    for header in headers:
                        table_content += f"<th>{header}</th>"
                    table_content += "</tr>"
                    for movie in movies:
                        table_content += "<tr>"
                        for col in movie:
                            table_content += (
                                f"<td>{col if col is not None else 'N/A'}</td>"
                            )
                        table_content += "</tr>"
                    table_content += "</table>"
                    content = table_content

        # Pass the content to the helper function to build the full page.
        full_page = render_full_html_page("Movies List (ex04)", content)
        return HttpResponse(full_page)

    except Exception as e:
        full_page = render_full_html_page("Error", f"An error occurred: {e}")
        return HttpResponse(full_page)


@csrf_exempt
def remove(request):
    """
    Handles form display and submission, using the helper for the HTML structure.
    """
    try:
        with get_connection() as conn:
            # Handle POST request for deletion
            if request.method == "POST":
                movie_title_to_remove = request.POST.get("title")
                if movie_title_to_remove:
                    with conn.cursor() as cursor:
                        cursor.execute(
                            "DELETE FROM ex04_movies WHERE title = %s;",
                            (movie_title_to_remove,),
                        )
                    conn.commit()

            # Display the form (for both GET and after POST)
            with conn.cursor() as cursor:
                cursor.execute("SELECT title FROM ex04_movies;")
                movies = cursor.fetchall()

                if not movies:
                    content = "No data available"
                else:
                    # Step 1: Build the unique content (the form).
                    form_content = '<form method="post">'
                    form_content += '<select name="title">'
                    for movie in movies:
                        form_content += (
                            f'<option value="{movie[0]}">{movie[0]}</option>'
                        )
                    form_content += "</select>"
                    form_content += (
                        '<button type="submit" name="remove">Remove</button>'
                    )
                    form_content += "</form>"
                    content = form_content

        # Pass the content to the helper to build the full page.
        full_page = render_full_html_page("Remove a Movie (ex04)", content)
        return HttpResponse(full_page)

    except Exception as e:
        full_page = render_full_html_page("Error", f"An error occurred: {e}")
        return HttpResponse(full_page)
