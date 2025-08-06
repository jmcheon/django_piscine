from django.db import models


class Movies(models.Model):
    # VARCHAR(64), UNIQUE and NOT NULL
    title = models.CharField(max_length=64, unique=True, null=False)
    # INTEGER and the PRIMARY KEY.
    episode_nb = models.IntegerField(primary_key=True)
    # TEXT type and can be NULL
    opening_crawl = models.TextField(null=True, blank=True)
    # VARCHAR(32) and NOT NULL
    director = models.CharField(max_length=32, null=False)
    # VARCHAR(128) and NOT NULL
    producer = models.CharField(max_length=128, null=False)
    # DATE type and NOT NULL
    release_date = models.DateField(null=False)

    def __str__(self):
        return self.title
