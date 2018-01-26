from datetime import timedelta

from django.db import models

# Here we will have model for categories of movies and a Movie Item


class MoviesCategories(models.Model):
    name = models.CharField(max_length=1200, null=False, unique=True)
    thumbnail = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Movie(models.Model):
    name = models.CharField(max_length=1000, null=False, unique=True)
    thumbnail = models.TextField(max_length=1200, null=False)
    source_url = models.CharField(max_length=5000, null=False)
    duration = models.TimeField(default=timedelta(hours=2))
    added_on = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(MoviesCategories, related_name="movies", on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('added_on',)
