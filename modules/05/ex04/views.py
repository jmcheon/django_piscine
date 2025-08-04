import psycopg2
from django.http import HttpResponse


def get_connection():
    """Fonction utilitaire pour la connexion à la BDD."""
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
    """Crée la table ex04_movies."""
    # Ce code est identique à celui de l'ex02, seul le nom de la table change.
    conn = get_connection()
    if not conn:
        return HttpResponse("Error: Could not connect to the database.")
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ex04_movies (
                    episode_nb INT PRIMARY KEY, title VARCHAR(64) UNIQUE NOT NULL,
                    opening_crawl TEXT, director VARCHAR(32) NOT NULL,
                    producer VARCHAR(128) NOT NULL, release_date DATE NOT NULL
                );
            """)
        conn.commit()
        return HttpResponse("OK")
    except Exception as e:
        return HttpResponse(f"Error: {e}")
    finally:
        conn.close()


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
                    results.append(f"OK: {movie['title']} inserted/re-inserted.")
                else:
                    results.append(f"OK: {movie['title']} already exists.")
        conn.commit()
        return HttpResponse("<br>".join(results))
    except Exception as e:
        return HttpResponse(f"An unexpected error occurred: {e}")
    finally:
        conn.close()


def display(request):
    """Affiche les données de la table."""
    # Ce code est identique à celui de l'ex02, avec le bon nom de table.
    conn = get_connection()
    if not conn:
        return HttpResponse("No data available")
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM ex04_movies;")
            movies = cursor.fetchall()
            if not movies:
                return HttpResponse("No data available")
            html = "<table border='1'><tr>"
            headers = [desc[0] for desc in cursor.description]
            for header in headers:
                html += f"<th>{header}</th>"
            html += "</tr>"
            for movie in movies:
                html += "<tr>"
                for col in movie:
                    html += f"<td>{col if col is not None else 'N/A'}</td>"
                html += "</tr>"
            html += "</table>"
            return HttpResponse(html)
    except Exception:
        return HttpResponse("No data available")
    finally:
        conn.close()


def remove(request):
    """Gère l'affichage et le traitement du formulaire de suppression."""
    conn = get_connection()
    if not conn:
        return HttpResponse("No data available")

    try:
        # Traitement de la soumission du formulaire
        if request.method == "POST":
            movie_title_to_remove = request.POST.get("movie_title")
            if movie_title_to_remove:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "DELETE FROM ex04_movies WHERE title = %s;",
                        (movie_title_to_remove,),
                    )
                conn.commit()

        # Affichage du formulaire (après une suppression ou en arrivant sur la page)
        with conn.cursor() as cursor:
            cursor.execute("SELECT title FROM ex04_movies;")
            movies = cursor.fetchall()

            if not movies:
                return HttpResponse("No data available")

            # Construction du formulaire HTML
            # Le formulaire est soumis à la même URL (action="")
            html = """
                <form method="post" action="">
                    <select name="movie_title">
            """
            for movie in movies:
                html += f'<option value="{movie[0]}">{movie[0]}</option>'

            html += """
                    </select>
                    <button type="submit">Remove</button>
                </form>
            """
            return HttpResponse(html)

    except Exception as e:
        return HttpResponse(f"An error occurred: {e}")
    finally:
        conn.close()
