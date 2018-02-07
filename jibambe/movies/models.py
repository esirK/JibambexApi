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
    duration = models.CharField(max_length=100, null=False)
    added_on = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(MoviesCategories, related_name="movies", on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('added_on',)


class Series(models.Model):
    name = models.CharField(max_length=1000, null=False, unique=True)
    thumbnail = models.TextField(max_length=1200, null=False)
    seasons_num = models.CharField(max_length=100, null=False, unique=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Series"


class Season(models.Model):
    """
    Model for a single season in a series
    """
    name = models.CharField(max_length=1000, null=False, unique=True)
    thumbnail = models.TextField(max_length=1200, null=False)
    num_episodes = models.CharField(max_length=100, null=False, unique=False)
    series = models.ForeignKey(Series, related_name="seasons", on_delete=models.CASCADE)

    def __str__(self):
        return self.name
