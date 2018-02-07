from django.contrib import admin

from .models import MoviesCategories, Movie, Series, Season

admin.site.register(MoviesCategories)
admin.site.register(Movie)
admin.site.register(Series)
admin.site.register(Season)
