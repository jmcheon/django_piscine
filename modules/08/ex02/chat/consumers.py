from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer

from .models import Message, Room


class ChatConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

        # history
        room = Room.objects.get(name=self.room_name)
        # Get the last 3 messages, ordered by timestamp
        last_messages = Message.objects.filter(room=room).order_by("-timestamp")[:3]

        # Send them one by one to the newly connected user
        for message in reversed(last_messages):  # reversed to send oldest first
            self.send_json(
                {
                    "message": message.content,
                    "username": message.author.username,
                }
            )

        # Announce that the user has joined the chat.
        username = self.scope["user"].username
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": f"{username} has joined the chat",
                "username": "System",  # We can assign this to a system user
            },
        )

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive_json(self, content):
        message_text = content.get("message", "")
        author = self.scope["user"]
        room_name = self.room_name

        # Find the room object
        room = Room.objects.get(name=room_name)

        # Create and save the new message object
        message = Message.objects.create(room=room, author=author, content=message_text)

        # Broadcast the message to the room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message.content,
                "username": message.author.username,
            },
        )

    # This method receives the message from the group and sends it to the browser.
    def chat_message(self, event):
        message = event["message"]
        username = event["username"]  # We get the username from the event

        # Send the message AND the username to the browser.
        self.send_json(
            {
                "message": message,
                "username": username,
            }
        )
