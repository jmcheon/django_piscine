from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer


class ChatConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

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

    # This method receives the message from a single browser.
    def receive_json(self, content):
        message = content.get("message", "")
        # Get the username from the authenticated user.
        print(self.scope["user"])
        username = self.scope["user"].username

        # Send the message AND the username to the room group.
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "username": username,
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
