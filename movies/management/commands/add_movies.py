from django.core.management import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    def handle(self, *args, **options):
        """
        Executes all commands required to populate an empty database with all movies in the harddisk.

        """
        clear_db = options['clear_db']

        if clear_db == 1:
            call_command("clear_database")
        call_command("populate_categories")
        call_command("populate_movies")
        call_command("populate_series")
        call_command("populate_seasons")
        call_command("populate_episodes")

    def add_arguments(self, parser):

        parser.add_argument('clear_db', type=int,
                            default=0,
                            nargs='?',
                            help='Clear the database first if the argument passed is 1')

