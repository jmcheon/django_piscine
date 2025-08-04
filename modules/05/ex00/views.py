import psycopg2
from django.http import HttpResponse


def init():
    try:
        # Connexion à la base de données
        conn = psycopg2.connect(
            dbname="formationdjango",
            user="djangouser",
            password="secret",
            host="localhost",  # ou l'IP de la VM
            port="5432",
        )
        cursor = conn.cursor()

        # Requête SQL pour créer la table si elle n'existe pas
        create_table_query = """
        CREATE TABLE IF NOT EXISTS ex00_movies (
            episode_nb INT PRIMARY KEY,
            title VARCHAR(64) UNIQUE NOT NULL,
            opening_crawl TEXT,
            director VARCHAR(32) NOT NULL,
            producer VARCHAR(128) NOT NULL,
            release_date DATE NOT NULL
        );
        """

        cursor.execute(create_table_query)
        conn.commit()

        # Fermeture de la connexion
        cursor.close()
        conn.close()

        return HttpResponse("OK")

    except Exception as e:
        # En cas d'erreur, on retourne un message décrivant le problème
        return HttpResponse(f"Error: {e}")
