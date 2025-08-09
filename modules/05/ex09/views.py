from django.http import HttpResponse
from django.shortcuts import render

from .models import People


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


def display(request):
    try:
        if not People.objects.exists():
            pass
    except Exception:
        full_page = render_full_html_page("", "No data available, please use the following command line before use: \n\npython3 manage.py loaddata ex09_initial_data.json")
        return HttpResponse(full_page)
    # This is the ORM query to get the required data.
    # 'homeworld__climate__icontains' is the Django ORM way to do a JOIN and a WHERE ... LIKE.
    # 'select_related' is an optimization to fetch the related Planet object in the same query.
    people = (
        People.objects.filter(homeworld__climate__icontains="windy")
        .order_by("name")
        .select_related("homeworld")
    )

    # Prepare context for the template.
    context = {
        "people": people,
        "loaddata_command": "python3 manage.py loaddata ex09_initial_data.json",
    }

    return render(request, "ex09/display.html", context)
