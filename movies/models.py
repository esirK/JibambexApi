from datetime import timedelta

from django.db import models


class MoviesCategories(models.Model):
    """
    Model for a single movie Category eg. Action, Animation, Horror etc.
    """
    name = models.CharField(max_length=250, null=False, unique=True)
    thumbnail = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Movie(models.Model):
    name = models.CharField(max_length=250, null=False, unique=True)
    thumbnail = models.TextField(max_length=1200, null=False)
    source_url = models.CharField(max_length=5000, null=False)
    duration = models.CharField(max_length=100, null=False)
    added_on = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(MoviesCategories, related_name="movies", on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name


class Series(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True)
    thumbnail = models.TextField(max_length=1200, null=False)
    seasons_num = models.CharField(max_length=100, null=False, unique=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Series"
        ordering = ('name',)


class Season(models.Model):
    """
    Model for a single season in a series
    """
    name = models.CharField(max_length=255, null=False, unique=True)
    thumbnail = models.TextField(max_length=255, null=False)
    num_episodes = models.CharField(max_length=100, null=False, unique=False)
    series = models.ForeignKey(Series, related_name="seasons", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Episode(models.Model):
    """
    Model for a single Episode in a season
    """
    name = models.CharField(max_length=1000, null=False, unique=False)
    thumbnail = models.TextField(max_length=1200, null=False)
    source_url = models.CharField(max_length=255, null=False, unique=True)
    duration = models.CharField(max_length=100, null=False)
    season = models.ForeignKey(Season, related_name="episodes", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)

