import urllib.parse

from django.core.management import BaseCommand

from jibambe.movies.models import MoviesCategories
from jibambe.movies.serializers import MoviesCategoriesSerializer, MovieSerializer

from termcolor import colored

import subprocess


class Command(BaseCommand):
    help = "Populates Database with movie data"

    def handle(self, *args, **options):
        import os
        url = "http://192.168.1.143:8000/static/movies/categories/"

        os.chdir('jibambe/movies/static/movies/categories')
        # List all directories in the categories folder
        categories = os.listdir('.')

        for category in range(0, len(categories)):
            category = categories[category]

            os.chdir(category)
            print(colored("Searching inside {0}", 'blue').format(category))

            # Loop through every file in the current directory

            for file in os.listdir('.'):

                # Loop through the directories of each category pick down its movies
                if os.path.isdir(file):
                    print("Files ", file)
                    self.stdout.write(self.style.WARNING("Found A directory!!!"
                                                         "looking for treasures in '{0}'".format(
                                                            category + "/" + file)))

                    # This directory hold movies so navigate it looking for movies

                    # Change directory into it
                    os.chdir(file)

                    print("All files inside here are {0}".format(os.listdir('.')))

                    # Filter the images i.e thumbnails out and the movies out.
                    # Create a url for them.
                    # Something like ['showdown-in-manila-movie-poster.jpg', 'showdown-in-manila-trailer-1_h480p.mov']
                    # get the thumbnail first
                    global movie_thumbnail

                    global source_url

                    global duration

                    global cat_id

                    for movie in os.listdir('.'):
                        if movie.endswith(".jpg") | movie.endswith(".png") | movie.endswith('.jpeg'):
                            movie_thumbnail = url + category + '/' + file + '/' + movie
                            # Encode the url
                            movie_thumbnail = urllib.parse.quote(movie_thumbnail, safe=":,/")

                            print('Thumbnail', movie_thumbnail)
                        # Get the movie source. i.e the Movie URL
                        if movie.lower().endswith(".mov") | movie.lower().endswith(".mp4") | movie.lower().endswith(
                                ".wav"):
                            source_url = url + category + '/' + file + '/' + movie
                            source_url = urllib.parse.quote(source_url, safe=":,/")

                            print('Source', source_url)

                            # Get movie duration
                            metadata = subprocess.Popen(["ffprobe", movie], stdout=subprocess.PIPE,
                                                        stderr=subprocess.STDOUT)

                            for stream in metadata.stdout.readlines():
                                stream = stream.decode("utf-8")
                                if "Duration" in stream:
                                    duration = stream.split(',')[0].split()[1]
                                    print("Thumbnail ", movie_thumbnail)
                                    cat = MoviesCategories.objects.filter(name=category).first()
                                    cat_id = cat.id

                    videos = MovieSerializer(
                        data={'name': movie[:-4], 'thumbnail': movie_thumbnail,
                              'source_url': source_url, 'duration': duration, 'category': cat_id})

                    print(colored("Trying to add '{0}' into {1}", 'magenta').format(
                        movie[:-4], category))
                    if videos.is_valid():
                        try:
                            videos.save()
                            print(colored('Successfully Added {0}', "green").format(movie))
                        except Exception as e:
                            print(colored("Error ", "red"), e)
                    else:
                        self.stderr.write(self.style.ERROR("Movie '{0}' not valid: {1}".
                                                           format(movie[:-4], videos.errors)))

                    os.chdir('..')
            os.chdir('..')