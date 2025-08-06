import psycopg2
from django.http import HttpResponse


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
    conn = get_connection()
    if not conn:
        return HttpResponse("Error: Could not connect to the database.")

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ex02_movies (
                    episode_nb INT PRIMARY KEY,
                    title VARCHAR(64) UNIQUE NOT NULL,
                    opening_crawl TEXT,
                    director VARCHAR(32) NOT NULL,
                    producer VARCHAR(128) NOT NULL,
                    release_date DATE NOT NULL
                );
            """)
        conn.commit()
        return HttpResponse("OK")
    except Exception as e:
        return HttpResponse(f"Error: {e}")
    finally:
        conn.close()


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
    """This view inserts data into the ex02_movies table."""
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
                try:
                    cursor.execute(
                        """
                        INSERT INTO ex02_movies (episode_nb, title, director, producer, release_date)
                        VALUES (%(episode_nb)s, %(title)s, %(director)s, %(producer)s, %(release_date)s)
                        ON CONFLICT (episode_nb) DO NOTHING;
                    """,
                        movie,
                    )
                    # ON CONFLICT permet d'éviter les erreurs si on relance populate.
                    # Le sujet n'impose pas de gestion de conflit, mais c'est une bonne pratique.

                    if cursor.rowcount > 0:
                        results.append(f"OK: {movie['title']} inserted.")
                    else:
                        results.append(f"OK: {movie['title']} already exists.")

                except Exception as e:
                    results.append(f"Error inserting {movie['title']}: {e}")
                    conn.rollback()  # Annule la transaction en cas d'erreur pour ce film
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
        full_page = render_full_html_page("Movies List (ex02)", content)
        return HttpResponse(full_page)

    except Exception as e:
        full_page = render_full_html_page("Error", f"An error occurred: {e}")
        return HttpResponse(full_page)
