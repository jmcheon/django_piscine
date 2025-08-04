from django.db import models


class Movies(models.Model):
    title = models.CharField(max_length=64, unique=True, null=False)
    episode_nb = models.IntegerField(primary_key=True)
    opening_crawl = models.TextField(null=True)
    director = models.CharField(max_length=32, null=False)
    producer = models.CharField(max_length=128, null=False)
    release_date = models.DateField(null=False)
    # Se met à jour uniquement lors de la création de l'objet
    created = models.DateTimeField(auto_now_add=True)
    # Se met à jour à chaque fois que l'objet est sauvegardé (.save())
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
