from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer

from .models import Message, Room

rooms = {}


class ChatConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        username = self.scope["user"].username

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

        # History
        room = Room.objects.get(name=self.room_name)
        last_messages = Message.objects.filter(room=room).order_by("-timestamp")[:3]
        for message in reversed(last_messages):
            self.send_json(
                {
                    "type": "chat_message",
                    "message": message.content,
                    "username": message.author.username,
                }
            )

        rooms.setdefault(self.room_name, set()).add(username)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {"type": "user_list", "users": list(rooms[self.room_name])},
        )

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": f"{username} has joined the chat",
                "username": "System",
            },
        )

    def disconnect(self, close_code):
        username = self.scope["user"].username

        if self.room_name in rooms and username in rooms[self.room_name]:
            rooms[self.room_name].remove(username)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {"type": "user_list", "users": list(rooms.get(self.room_name, set()))},
        )

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": f"{username} has left the chat",
                "username": "System",
            },
        )

        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive_json(self, content):
        message_text = content.get("message", "")
        author = self.scope["user"]
        room = Room.objects.get(name=self.room_name)

        message = Message.objects.create(room=room, author=author, content=message_text)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message.content,
                "username": message.author.username,
            },
        )

    def chat_message(self, event):
        self.send_json(
            {
                "type": "chat_message",
                "message": event["message"],
                "username": event["username"],
            }
        )

    def user_list(self, event):
        self.send_json({"type": "user_list", "users": event["users"]})
