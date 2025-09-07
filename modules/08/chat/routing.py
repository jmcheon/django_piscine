from django.urls import re_path

from . import consumers

# This list defines the WebSocket URL patterns.
websocket_urlpatterns = [
    # This regular expression matches URLs like /ws/chat/room_name/
    # and passes the room_name to the consumer.
    re_path(r"ws/chat/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
]
