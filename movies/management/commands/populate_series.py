import urllib

from django.core.management import BaseCommand
from termcolor import colored

from movies.serializers import SerieSerializer


class Command(BaseCommand):
    help = "Populates Database with Different series"

    def handle(self, *args, **options):
        import os
        os.chdir(os.getenv("STATIC")+'/static/series')
        # List all directories in the series folder
        series = os.listdir('.')

        url = os.getenv("IP")+"/static/series/"
        thumbnail = ""

        for single_series in series:
            if single_series.startswith("."):
                continue
            # Pick the series name and inside its folder, pick its thumbnail
            os.chdir(single_series)
            seasons = os.listdir('.')  # All seasons are contained inside a single series folder

            num_seasons = len(seasons)

            for season in seasons:
                if season.endswith(".jpg") | season.endswith(".png") | season.endswith('.jpeg'):
                    num_seasons -= 1
                    # Its the series thumbnail
                    print("Found a thumbnail... ", season)
                    thumbnail = url + single_series + '/' + season
                    thumbnail = urllib.parse.quote(thumbnail, safe=":,/")

            series_found = SerieSerializer(data={'name': single_series, 'thumbnail': thumbnail,
                                                 'seasons': num_seasons})

            print(colored("Trying to add `" + single_series + "` to database", "yellow"))

            if series_found.is_valid():
                try:
                    series_found.save()
                    print(colored('Successfully Populated database with {0}  Series'
                                  , "green").format(single_series))
                except Exception as e:
                    print(colored("Error ", "red"), e)
            else:
                self.stderr.write(self.style.ERROR("Series '{0}' not valid: {1}".
                                                   format(single_series, series_found.errors)))
            # navigate back one dir up
            os.chdir('..')
