from rest_framework import serializers

from jibambe.movies.models import MoviesCategories, Movie


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
