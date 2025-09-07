from django.urls import path

from . import views

urlpatterns = [
    # URL for the lobby page, which lists all rooms.
    path("", views.lobby_view, name="lobby"),

    # URL for an individual chat room.
    path('<str:room_name>/', views.room_view, name='room'),
]
