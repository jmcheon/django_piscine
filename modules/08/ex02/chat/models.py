from django.conf import settings
from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Message(models.Model):
    # The room where the message was sent
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    # The user who sent the message
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # The content of the message
    content = models.TextField()
    # The timestamp when the message was created
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username}: {self.content}"

    # This helps in ordering the messages
    class Meta:
        ordering = ["timestamp"]
