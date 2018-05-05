import urllib

from django.core.management import BaseCommand
from termcolor import colored

from movies.models import Series
from movies.serializers import SingleSeasonSerializer


class Command(BaseCommand):
    help = "Populates Database with Different series"

    def handle(self, *args, **options):
        import os
        os.chdir(os.getenv("STATIC")+'/static/series')
        # List all directories in the series folder
        series = os.listdir('.')

        url = os.getenv("IP")+"/static/series/"

        for single_series in series:
            # Pick the series name and inside its folder, pick its thumbnail
            os.chdir(single_series)
            seasons = os.listdir('.')  # All seasons are contained inside a single series folder

            for season in seasons:
                if season.endswith(".jpg") | season.endswith(".png") | season.endswith('.jpeg'):
                    # Its the series thumbnail
                    print("Found a thumbnail... ", season)
                else:
                    print("Found a seasons folder ", season)
                    # Go through the seasons folder, pick up the seasons and add them to db
                    os.chdir(season)
                    num_episodes = len(os.listdir('.'))
                    season_thumbnail = ''
                    season_episodes = []
                    for single_season in os.listdir('.'):
                        if single_season.endswith(".jpg") | single_season.endswith(".png") | single_season.endswith(
                                '.jpeg'):
                            num_episodes -= 1
                            season_thumbnail = url + single_series + '/' + single_season
                            season_thumbnail = urllib.parse.quote(season_thumbnail, safe=":,/")

                        else:
                            season_episodes.append(single_series)

                    # Get the series object this season is under and pick its id
                    series = Series.objects.filter(name=single_series).first()
                    if series:
                        seasons_found = SingleSeasonSerializer(data={'name': single_series+' '+season,
                                                                     'thumbnail': season_thumbnail,
                                                                     'num_episodes': len(season_episodes),
                                                                     'series': series.id})
                    else:
                        print(colored("Error!!! Ensure you have run `polpulate_series` "
                                      "first before running the `populate_seasons command`", "red"))
                        os.chdir('..')
                        break
                    if seasons_found.is_valid():
                        try:
                            seasons_found.save()
                            print(colored('Successfully Populated database with {0}  Season'
                                          , "green").format(season))
                        except Exception as e:
                            print(colored("Error ", "red"), e)
                    else:
                        self.stderr.write(self.style.ERROR("Season '{0}' not valid: {1}".
                                                           format(season, seasons_found.errors)))
                    os.chdir('..')

            # navigate back one dir up
            os.chdir('..')
