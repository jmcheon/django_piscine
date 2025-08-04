from django.http import HttpResponse
from django.shortcuts import render

from .models import People


def display(request):
    """
    Affiche les personnages des planètes venteuses en utilisant l'ORM.
    """
    # On filtre les personnages (People) en se basant sur un champ
    # de leur planète (homeworld). La magie de l'ORM !
    # `homeworld__climate__icontains` traverse la relation ForeignKey.
    # `__icontains` est un "LIKE" insensible à la casse.
    # `select_related('homeworld')` optimise la requête en faisant une jointure SQL.
    people = (
        People.objects.select_related("homeworld")
        .filter(homeworld__climate__icontains="windy")
        .order_by("name")
    )

    if not people.exists():
        # Affiche le message et la commande à exécuter si la base est vide.
        command = "python3 manage.py loaddata ex09_initial_data.json"
        return HttpResponse(
            f"No data available, please use the following command line before use:<br><code>{command}</code>"
        )

    return render(request, "ex09/display.html", {"people": people})
