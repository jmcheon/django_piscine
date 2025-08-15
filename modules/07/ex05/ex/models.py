from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Article(models.Model):
    # The article's title, max 64 chars, cannot be null.
    title = models.CharField(max_length=64, null=False, verbose_name=_("Title"))

    # A reference to the User model, cannot be null.
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=False)

    # The creation timestamp, automatically set, cannot be null.
    created = models.DateTimeField(auto_now_add=True, null=False)

    # A short summary, max 312 chars, cannot be null.
    synopsis = models.CharField(max_length=312, null=False, verbose_name=_("Synopsis"))

    content = models.TextField(null=False, verbose_name=_("Content"))

    def __str__(self):
        return self.title


class UserFavouriteArticle(models.Model):
    # A reference to the User model, cannot be null.
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    # A reference to the Article model, cannot be null.
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=False)

    class Meta:
        # This ensures that a combination of a user and an article must be unique in the database table.
        unique_together = ("user", "article")

    def __str__(self):
        return self.article.title
