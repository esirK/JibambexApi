from django.core.management import BaseCommand
from django.db import connection


class Command(BaseCommand):
    def handle(self, *args, **options):

        with connection.cursor() as cursor:
            # Delete all movies in all categories and reset the counter to 0
            cursor.execute("delete from movies_movie")
            cursor.execute("ALTER TABLE movies_movie AUTO_INCREMENT=0;")

            print("Deleted all Movies from Database :)")

            # Delete all movie categories
            cursor.execute("delete from movies_moviescategories")
            cursor.execute("ALTER TABLE movies_moviescategories AUTO_INCREMENT=0;")

            print("Deleted all Movie Categories from Database :)")

            # Delete all episodes of all seasons available
            cursor.execute("delete from movies_episode")
            cursor.execute("ALTER TABLE movies_episode AUTO_INCREMENT=0;")

            print("Deleted all episodes from Database :)")

            # Delete all seasons of every series in the database
            cursor.execute("delete from movies_season")
            cursor.execute("ALTER TABLE movies_season AUTO_INCREMENT=0;")
            print("Deleted all seasons from Database :)")

            # Delete all series in the database
            cursor.execute("delete from movies_series")
            cursor.execute("ALTER TABLE movies_series AUTO_INCREMENT=0;")

            print(cursor.fetchall())
        pass
