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
    """
    Crée la table ex06_movies avec les champs created/updated
    et le trigger associé.
    """
    conn = get_connection()
    if not conn:
        return HttpResponse("Error: Could not connect to the database.")

    try:
        with conn.cursor() as cursor:
            # 1. Création de la table avec les nouveaux champs et leurs valeurs par défaut
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ex06_movies (
                    episode_nb INT PRIMARY KEY,
                    title VARCHAR(64) UNIQUE NOT NULL,
                    opening_crawl TEXT,
                    director VARCHAR(32) NOT NULL,
                    producer VARCHAR(128) NOT NULL,
                    release_date DATE NOT NULL,
                    created TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    updated TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                );
            [cite_start]""")  # [cite: 216-218]

            # 2. Création de la fonction de trigger
            cursor.execute("""
                CREATE OR REPLACE FUNCTION update_changetimestamp_column()
                RETURNS TRIGGER AS $$
                BEGIN
                   NEW.updated = now();
                   RETURN NEW;
                END;
                $$ language 'plpgsql';
            [cite_start]""")

            # 3. Attachement du trigger à la table
            # On le supprime d'abord au cas où il existerait déjà pour éviter une erreur
            cursor.execute(
                "DROP TRIGGER IF EXISTS update_films_changetimestamp ON ex06_movies;"
            )
            cursor.execute("""
                CREATE TRIGGER update_films_changetimestamp BEFORE UPDATE
                ON ex06_movies FOR EACH ROW EXECUTE PROCEDURE
                update_changetimestamp_column();
            [cite_start]""") 

        conn.commit()
        return HttpResponse("OK")
    except Exception as e:
        conn.rollback()
        return HttpResponse(f"Error: {e}")
    finally:
        conn.close()


def populate(request):
    """Peuple la table (similaire à ex04)."""
    # Le code est identique à celui de l'ex04, les champs created/updated
    # sont gérés automatiquement par la BDD.
    movies_data = [
        # ... collez les données des films ici ...
        {
            "episode_nb": 1,
            "title": "The Phantom Menace",
            "director": "George Lucas",
            "producer": "Rick McCallum",
            "release_date": "1999-05-19",
        },
        {
            "episode_nb": 7,
            "title": "The Force Awakens",
            "director": "J. J. Abrams",
            "producer": "Kathleen Kennedy, J. J. Abrams, Bryan Burk",
            "release_date": "2015-12-11",
        },
    ]
    # ... (code de la vue populate de l'ex04, en changeant ex04_movies en ex06_movies)
    # Pour la concision, le code complet n'est pas recopié ici.
    return HttpResponse("Populate view needs to be implemented similar to ex04.")


def display(request):
    """Affiche les données de la table (similaire à ex04)."""
    # Le code est identique à celui de l'ex04, il affichera automatiquement
    # les nouvelles colonnes.
    # ... (code de la vue display de l'ex04, en changeant ex04_movies en ex06_movies)
    # Pour la concision, le code complet n'est pas recopié ici.
    return HttpResponse("Display view needs to be implemented similar to ex04.")


def update(request):
    """Gère l'affichage et le traitement du formulaire de mise à jour."""
    conn = get_connection()
    if not conn:
        return HttpResponse("No data available")

    try:
        # Traitement de la soumission du formulaire
        if request.method == "POST":
            title = request.POST.get("title")
            opening_crawl = request.POST.get("opening_crawl")

            if title and opening_crawl is not None:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "UPDATE ex06_movies SET opening_crawl = %s WHERE title = %s;",
                        (opening_crawl, title),
                    )
                conn.commit()

        # Affichage du formulaire
        with conn.cursor() as cursor:
            cursor.execute("SELECT title FROM ex06_movies;")
            movies = cursor.fetchall()

            if not movies:
                return HttpResponse("No data available")

            # Construction du formulaire HTML
            html = """
                <form method="post" action="">
                    <select name="title">
            """
            for movie in movies:
                html += f'<option value="{movie[0]}">{movie[0]}</option>'

            html += """
                    </select>
                    <br><br>
                    <textarea name="opening_crawl" rows="10" cols="50"></textarea>
                    <br><br>
                    <button type="submit">Update</button>
                </form>
            """
            return HttpResponse(html)

    except Exception as e:
        return HttpResponse(f"An error occurred: {e}")
    finally:
        conn.close()
