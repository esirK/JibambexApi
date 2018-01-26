import urllib

from django.core.management import BaseCommand
from termcolor import colored

from jibambe.movies.serializers import MoviesCategoriesSerializer


class Command(BaseCommand):
    help = "Populates Database with movie data"

    def handle(self, *args, **options):
        # Loop through 'static/movies/categories' picking the category name and and image
        import os
        url = "http://192.168.1.143:8000/static/movies/categories/"

        os.chdir('jibambe/movies/static/movies/categories')
        # List all directories in the categories folder
        categories = os.listdir('.')

        for category in range(0, len(categories)):
            category = categories[category]
            # Loop through each category picking its name and its thumbnail
            os.chdir(category)
            print(colored("Searching inside {0}", 'blue').format(category))

            # Loop through every file in the current directory

            for file in os.listdir('.'):
                if file.endswith(".jpg") | file.endswith(".png") | file.endswith('.jpeg'):
                    thumbnail = url + category + '/' + file
                    thumbnail = urllib.parse.quote(thumbnail, safe=":,/")
                    self.stdout.write(self.style.WARNING("Found a thumbnail {0}".format(thumbnail)))
                    movies_category = MoviesCategoriesSerializer(data={'name': category, 'thumbnail': thumbnail})

                    print(colored("Trying to add Movie Category '{0}' into database", 'magenta').format(category))
                    if movies_category.is_valid():
                        try:
                            movies_category.save()
                            print(colored('Successfully Populated database with {0} Movie '
                                          'Category ', "green").format(category))
                        except Exception as e:
                            print(colored("Error ", "red"), e)
                    else:
                        self.stderr.write(self.style.ERROR("Movie Category '{0}' not valid: {1}".
                                                           format(category, movies_category.errors)))
            os.chdir('..')
