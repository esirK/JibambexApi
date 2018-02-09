from rest_framework import serializers

from .models import MoviesCategories, Movie, Series, Season, Episode


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('name', 'thumbnail', 'source_url', 'duration', 'category')


class MoviesCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoviesCategories
        fields = ('name', 'id', 'thumbnail')


class SingleCategorySerializer(serializers.ModelSerializer):
    movies = MovieSerializer(many=True, read_only=True)

    class Meta:
        model = MoviesCategories
        fields = ('movies',)


class SingleSeasonSerializer(serializers.ModelSerializer):
    """
    Serializer for single Season
    """
    class Meta:
        model = Season
        fields = ('name', 'thumbnail', 'num_episodes', 'series', 'id')


class SerieSerializer(serializers.ModelSerializer):
    seasons = SingleSeasonSerializer(many=True, read_only=True)
    """Serializer for the Series model"""
    class Meta:
        model = Series
        fields = ('name', 'thumbnail', 'seasons', 'id')


class EpisodeSerializer(serializers.ModelSerializer):
    """
    Serializer for a single episode
    """
    class Meta:
        model = Episode
        fields = ('name', 'thumbnail', 'source_url', "duration", "season")
