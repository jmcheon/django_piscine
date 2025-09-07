from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Room


def lobby_view(request):
    """
    This view lists all available chat rooms.
    """
    # Query all Room objects from the database.
    rooms = Room.objects.all()

    # Pass the rooms to the template through the context dictionary.
    context = {
        "rooms": rooms,
    }
    return render(request, "chat/lobby.html", context)


@login_required
def room_view(request, room_name):
    """
    This view renders the chat room page itself.
    """
    # Find the room object. If not found, this will raise a 404 error.
    room = Room.objects.get(name=room_name)

    # Pass the room name and room object to the template.
    context = {
        "room_name": room_name,
        "room": room,
    }
    return render(request, "chat/room.html", context)
