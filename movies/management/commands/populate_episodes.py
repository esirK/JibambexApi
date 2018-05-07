import subprocess
import urllib

from django.core.management import BaseCommand
from termcolor import colored

from movies.models import Season
from movies.serializers import EpisodeSerializer


class Command(BaseCommand):
    help = "Populates Database with Different episodes of a single season of a single series"

    def handle(self, *args, **options):
        import os
        os.chdir(os.getenv("STATIC")+'/static/series')
        # List all directories in the series folder
        series = os.listdir('.')

        url = os.getenv("IP")+"/static/series/"

        for single_series in series:

            if single_series.startswith("."):
                continue

            os.chdir(single_series)
            seasons = os.listdir('.')  # All seasons are contained inside a single series folder

            for season in seasons:

                if season.endswith(".jpg") | season.endswith(".png") | season.endswith('.jpeg'):
                    # Its the series thumbnail
                    print("Found a thumbnail... ", season)
                else:
                    print("Found a seasons folder ", season)

                    # Get the season object the single_series is under and pick its id

                    series_season = Season.objects.filter(name=single_series + ' ' + season).first()

                    # Go through the seasons folder, pick up the seasons and add them to db
                    os.chdir(season)
                    episode_thumbnail = ''

                    for episode in os.listdir('.'):
                        if episode.endswith(".jpg") | episode.endswith(".png") | episode.endswith(
                                '.jpeg'):
                            episode_thumbnail = url + single_series + '/' + episode

                            episode_thumbnail = urllib.parse.quote(episode_thumbnail, safe=":,/")
                    for episode in os.listdir('.'):
                        if not (episode.endswith(".jpg") | episode.endswith(".png") | episode.endswith(
                                '.jpeg')):
                            # The real episodes

                            # Get the duration of the episodes
                            duration = '-- : -- : --  --'

                            metadata = subprocess.Popen(["ffprobe", episode], stdout=subprocess.PIPE,
                                                        stderr=subprocess.STDOUT)

                            for stream in metadata.stdout.readlines():
                                stream = stream.decode("utf-8")
                                if 'Duration' in stream:
                                    duration = stream.split(',')[0].split()[1]

                            source_url = url + single_series + '/' + season + '/' + episode
                            source_url = urllib.parse.quote(source_url, safe=":,/")

                            print("Duration Is ", duration)

                            episode_found = EpisodeSerializer(data={'name': episode[:-4],
                                                                    'thumbnail': episode_thumbnail,
                                                                    'source_url': source_url,
                                                                    'duration': duration[:-3],
                                                                    'season': series_season.id})

                            if episode_found.is_valid():
                                try:
                                    episode_found.save()
                                    print(colored('Successfully Populated database with {0} '
                                                  , "green").format(episode))

                                except Exception as e:
                                    print(colored("Error ", "red"), e)
                            else:
                                self.stderr.write(self.style.ERROR("Episode '{0}' not valid: {1}".
                                                                   format(episode, episode_found.errors)))

                    os.chdir('..')

            # navigate back one dir up
            os.chdir('..')
