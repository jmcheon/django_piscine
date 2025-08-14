from django.conf import settings
from django.db import models


class Tip(models.Model):
    contenu = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    auteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # We store the user list who upvoted
    upvotes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="upvoted_tips", blank=True
    )
    # We store the user list who downvoted
    downvotes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="downvoted_tips", blank=True
    )

    def __str__(self):
        return f"Tip by {self.auteur.username} on {self.date.strftime('%Y-%m-%d')}"

    # to defined the permission
    class Meta:
        permissions = [
            ("can_downvote_tip", "Can downvote a tip"),
        ]
