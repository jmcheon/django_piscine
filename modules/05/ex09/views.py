from django.shortcuts import render

from .models import People


def display(request):
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
