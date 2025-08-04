import os

import psycopg2
from django.conf import settings
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
    """Crée les tables planets et people avec une clé étrangère."""
    conn = get_connection()
    if not conn:
        return HttpResponse("Error: Could not connect to the database.")

    # La table 'planets' doit être créée avant 'people' à cause de la clé étrangère.
    create_planets_table = """
        CREATE TABLE IF NOT EXISTS ex08_planets (
            id SERIAL PRIMARY KEY,
            name VARCHAR(64) UNIQUE NOT NULL,
            climate VARCHAR(255),
            diameter INT,
            orbital_period INT,
            population BIGINT,
            rotation_period INT,
            surface_water REAL,
            terrain VARCHAR(128)
        );
    """
    create_people_table = """
        CREATE TABLE IF NOT EXISTS ex08_people (
            id SERIAL PRIMARY KEY,
            name VARCHAR(64) UNIQUE NOT NULL,
            birth_year VARCHAR(32),
            gender VARCHAR(32),
            eye_color VARCHAR(32),
            hair_color VARCHAR(32),
            height INT,
            mass REAL,
            homeworld VARCHAR(64) REFERENCES ex08_planets(name)
        );
    """

    try:
        with conn.cursor() as cursor:
            cursor.execute(create_planets_table)
            cursor.execute(create_people_table)
        conn.commit()
        return HttpResponse("OK")
    except Exception as e:
        conn.rollback()
        return HttpResponse(f"Error: {e}")
    finally:
        conn.close()


def populate(request):
    """
    Peuple les tables en utilisant la méthode copy_from pour importer les CSV.
    """
    conn = get_connection()
    if not conn:
        return HttpResponse("Error: Could not connect to the database.")

    # Chemin vers les fichiers CSV
    planets_csv_path = os.path.join(settings.BASE_DIR, "ex08", "static", "planets.csv")
    people_csv_path = os.path.join(settings.BASE_DIR, "ex08", "static", "people.csv")

    results = []

    try:
        with conn.cursor() as cursor:
            # Peupler la table des planètes
            try:
                with open(planets_csv_path, "r") as f:
                    # On ignore l'en-tête (header) du CSV
                    next(f)
                    # La magie de copy_from : rapide et efficace
                    cursor.copy_from(
                        f,
                        "ex08_planets",
                        sep=",",
                        columns=(
                            "name",
                            "climate",
                            "diameter",
                            "orbital_period",
                            "population",
                            "rotation_period",
                            "surface_water",
                            "terrain",
                        ),
                    )
                results.append("planets.csv: OK")
            except Exception as e:
                results.append(f"planets.csv: Error - {e}")
                raise  # Stoppe la transaction si le premier fichier échoue

            # Peupler la table des personnages
            try:
                with open(people_csv_path, "r") as f:
                    next(f)
                    cursor.copy_from(
                        f,
                        "ex08_people",
                        sep=",",
                        columns=(
                            "name",
                            "birth_year",
                            "gender",
                            "eye_color",
                            "hair_color",
                            "height",
                            "mass",
                            "homeworld",
                        ),
                    )
                results.append("people.csv: OK")
            except Exception as e:
                results.append(f"people.csv: Error - {e}")

        conn.commit()
        return HttpResponse("<br>".join(results))
    except Exception as e:
        conn.rollback()
        results.append(f"Transaction failed: {e}")
        return HttpResponse("<br>".join(results))
    finally:
        conn.close()


def display(request):
    """
    Affiche les personnages des planètes venteuses en joignant les tables.
    """
    conn = get_connection()
    if not conn:
        return HttpResponse("No data available")

    query = """
        SELECT p.name, pl.name, pl.climate
        FROM ex08_people p
        JOIN ex08_planets pl ON p.homeworld = pl.name
        WHERE pl.climate LIKE '%windy%'
        ORDER BY p.name ASC;
    """

    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()

            if not results:
                return HttpResponse("No data available")

            # Construction du tableau HTML
            html = "<table border='1'><tr><th>Character</th><th>Homeworld</th><th>Climate</th></tr>"
            for row in results:
                html += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td></tr>"
            html += "</table>"

            return HttpResponse(html)

    except Exception:
        return HttpResponse("No data available")
    finally:
        conn.close()
