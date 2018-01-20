from django.contrib import admin

from .models import MoviesCategories, Movie

admin.site.register(MoviesCategories)
admin.site.register(Movie)
