from django.conf import settings
from django.contrib.auth.models import AbstractUser
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


class CustomUser(AbstractUser):
    @property
    def reputation(self):
        score = 0
        for tip in self.tip_set.all():
            score += tip.upvotes.count() * 5
            score -= tip.downvotes.count() * 2
        return score

    def has_perm(self, perm, obj=None):
        """
        Custom permission handling based on reputation.
        """
        # A user with 15 reputation can downvote tips.
        if perm == "ex.can_downvote_tip":
            return self.reputation >= 15

        # A user with 30 reputation can delete tips.
        if perm == "ex.delete_tip":
            return self.reputation >= 30

        # For all other permissions, fall back to the default behavior.
        # This is CRUCIAL for superuser rights, admin access, etc.
        return super().has_perm(perm, obj)
