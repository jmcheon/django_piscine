from django.db import models


class Movies(models.Model):
    # These fields are the same as in ex01/ex03/ex05.
    title = models.CharField(max_length=64, unique=True, null=False)
    episode_nb = models.IntegerField(primary_key=True)
    opening_crawl = models.TextField(null=True, blank=True)
    director = models.CharField(max_length=32, null=False)
    producer = models.CharField(max_length=128, null=False)
    release_date = models.DateField(null=False)

    # auto_now_add=True sets this field to the current time only when the object is first created.
    # This is the ORM equivalent of a default value for creation timestamp.
    created = models.DateTimeField(auto_now_add=True)

    # auto_now=True updates this field to the current time every time the object's .save() method is called.
    # This is the ORM equivalent of the database trigger from ex06.
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
