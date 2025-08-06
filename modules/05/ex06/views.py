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
    """
    Creates the ex06_movies table with two new timestamp fields,
    and a PostgreSQL function and trigger to automatically update the 'updated' field.
    """
    # SQL to create the table, now with 'created' and 'updated' fields.
    sql_create_table = """
    CREATE TABLE IF NOT EXISTS ex06_movies (
        episode_nb      INT PRIMARY KEY,
        title           VARCHAR(64) UNIQUE NOT NULL,
        opening_crawl   TEXT,
        director        VARCHAR(32) NOT NULL,
        producer        VARCHAR(128) NOT NULL,
        release_date    DATE NOT NULL,
        created         TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
        updated         TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
    );
    """

    # SQL for the trigger function
    sql_create_function = """
    CREATE OR REPLACE FUNCTION update_changetimestamp_column()
    RETURNS TRIGGER AS $$
    BEGIN
        NEW.updated = NOW();
        NEW.created = OLD.created;
        RETURN NEW;
    END;
    $$ language 'plpgsql';
    """

    # SQL to create the trigger itself
    # We add DROP TRIGGER to make the init script safely re-runnable.
    sql_create_trigger = """
    DROP TRIGGER IF EXISTS update_films_changetimestamp ON ex06_movies;
    CREATE TRIGGER update_films_changetimestamp BEFORE UPDATE
    ON ex06_movies FOR EACH ROW EXECUTE PROCEDURE
    update_changetimestamp_column();
    """

    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql_create_table)
                cursor.execute(sql_create_function)
                cursor.execute(sql_create_trigger)
        return HttpResponse("OK")
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}")


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
    Populates the ex06_movies table with the data from ex02.
    The 'created' and 'updated' fields will be set by default.
    """
    movies_to_insert = [
        # Data is the same as ex02
        (1, "The Phantom Menace", "George Lucas", "Rick McCallum", "1999-05-19"),
        (2, "Attack of the Clones", "George Lucas", "Rick McCallum", "2002-05-16"),
        (3, "Revenge of the Sith", "George Lucas", "Rick McCallum", "2005-05-19"),
        (4, "A New Hope", "George Lucas", "Gary Kurtz, Rick McCallum", "1977-05-25"),
        (
            5,
            "The Empire Strikes Back",
            "Irvin Kershner",
            "Gary Kurtz, Rick McCallum",
            "1980-05-17",
        ),
        (
            6,
            "Return of the Jedi",
            "Richard Marquand",
            "Howard G. Kazanjian, George Lucas, Rick McCallum",
            "1983-05-25",
        ),
        (
            7,
            "The Force Awakens",
            "J. J. Abrams",
            "Kathleen Kennedy, J. J. Abrams, Bryan Burk",
            "2015-12-11",
        ),
    ]

    # We specify the columns to insert into, letting the database handle the new fields.
    sql_insert = """
    INSERT INTO ex06_movies (episode_nb, title, director, producer, release_date)
    VALUES (%s, %s, %s, %s, %s) ON CONFLICT (episode_nb) DO NOTHING;
    """

    results = []
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                for movie in movies_to_insert:
                    try:
                        cursor.execute(sql_insert, movie)
                        results.append("OK<br>")
                    except Exception:
                        pass  # Ignore errors on individual inserts
        return HttpResponse(
            "".join(results) if results else "All movies already populated."
        )
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}")


def display(request):
    """
    Displays all data from the ex06_movies table.
    """
    # This will dynamically show the new 'created' and 'updated' columns.
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM ex06_movies ORDER BY episode_nb;")
                movies = cursor.fetchall()

                if not movies:
                    content = "No data available"
                else:
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

        full_page = render_full_html_page("Movies List (ex06)", content)
        return HttpResponse(full_page)
    except Exception as e:
        full_page = render_full_html_page("Error", f"An error occurred: {e}")
        return HttpResponse(full_page)


@csrf_exempt
def update(request):
    """
    Handles form display and submission to update a movie's opening_crawl.
    """
    try:
        with get_connection() as conn:
            # Handle POST request to perform the update
            if request.method == "POST":
                title_to_update = request.POST.get("title")
                new_crawl_text = request.POST.get("opening_crawl")

                if title_to_update and new_crawl_text is not None:
                    with conn.cursor() as cursor:
                        sql_update = "UPDATE ex06_movies SET opening_crawl = %s WHERE title = %s;"
                        cursor.execute(sql_update, (new_crawl_text, title_to_update))
                    conn.commit()

            # Display the form (for both GET and after POST)
            with conn.cursor() as cursor:
                cursor.execute("SELECT title FROM ex06_movies;")
                movies = cursor.fetchall()

                if not movies:
                    return HttpResponse("No data available")

                # Build the HTML form with a dropdown and a text field.
                form_content = '<form method="post">'
                form_content += '<select name="title">'
                for movie in movies:
                    form_content += f'<option value="{movie[0]}">{movie[0]}</option>'
                form_content += "</select><br><br>"
                form_content += '<textarea name="opening_crawl" rows="4" cols="50"></textarea><br><br>'
                form_content += '<button type="submit">Update</button>'
                form_content += "</form>"

        full_page = render_full_html_page("Update Movie (ex06)", form_content)
        return HttpResponse(full_page)

    except Exception as e:
        full_page = render_full_html_page("Error", f"An error occurred: {e}")
        return HttpResponse(full_page)
