import os

import psycopg2
from django.conf import settings
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


def init(request):
    """
    Creates two tables, ex08_planets and ex08_people, with a foreign key relationship.
    """
    sql_planets = """
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
    sql_people = """
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
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql_planets)
                cursor.execute(sql_people)
        return HttpResponse("OK")
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}")


def populate(request):
    """
    Populates the tables using data from TAB-separated files.
    """
    results = []
    # Path to the CSV/TSV files at the root of the project
    planets_csv_path = os.path.join(settings.BASE_DIR, "planets.csv")
    people_csv_path = os.path.join(settings.BASE_DIR, "people.csv")

    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                # --- Populate planets table ---
                with open(planets_csv_path, "r") as f:
                    cursor.copy_from(
                        f,
                        "ex08_planets",
                        sep="\t",
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
                        null="NULL",
                    )
                results.append("OK for planets.csv<br>")

                # --- Populate people table ---
                with open(people_csv_path, "r") as f:
                    cursor.copy_from(
                        f,
                        "ex08_people",
                        sep="\t",
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
                        null="NULL",
                    )
                results.append("OK for people.csv<br>")

        return HttpResponse("".join(results))
    except psycopg2.DataError as e:
        return HttpResponse(f"Data formatting error in CSV file: {e}")
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}")


def display(request):
    """
    Displays characters from windy planets.
    Handles the case where the table does not exist gracefully.
    """
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                sql_join_query = """
                SELECT
                    p.name, p.homeworld, pl.climate
                FROM
                    ex08_people p
                JOIN
                    ex08_planets pl ON p.homeworld = pl.name
                WHERE
                    pl.climate LIKE '%%windy%%'
                ORDER BY
                    p.name ASC;
                """
                cursor.execute(sql_join_query)
                results = cursor.fetchall()

                if not results:
                    content = "No data available"
                else:
                    # Build the HTML table...
                    table_content = "<table border='1'>"
                    table_content += "<tr><th>Character Name</th><th>Homeworld</th><th>Climate</th></tr>"
                    for row in results:
                        table_content += "<tr>"
                        for col in row:
                            table_content += f"<td>{col}</td>"
                        table_content += "</tr>"
                    table_content += "</table>"
                    content = table_content

        # If everything in the 'try' block succeeds, build and return the page.
        full_page = render_full_html_page("Characters from Windy Planets", content)
        return HttpResponse(full_page)

    except psycopg2.errors.UndefinedTable:
        # This 'except' block specifically catches the "table does not exist" error.
        # It then displays the user-friendly message as required.
        content = "No data available (Hint: The table does not exist. Please visit the init page first.)"
        full_page = render_full_html_page("Display", content)
        return HttpResponse(full_page)

    except Exception as e:
        # This catches any other potential errors.
        content = f"An unexpected error occurred: {e}"
        full_page = render_full_html_page("Error", content)
        return HttpResponse(full_page)
