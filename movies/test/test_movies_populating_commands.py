from django.test import TestCase, Client
from django.core import management


class TestMoviesPopulatingCommands(TestCase):
    """
    Tests if the commands defined in the movies management/commands package
    WORKS as expected.
    """

    def setUp(self):
        self.client = Client()

    def test_populate_moviescategories(self):
        """
        Tests if moviescategories returns all movies categories
         created by populate_moviescategories command
        """
        response = self.client.get("/moviescategories/")
        self.assertEqual([], response.data)

        # Add movies categories
        management.call_command("populate_categories")
        response = self.client.get("/moviescategories/")

        self.assertGreater(len(response.data), 0)

    def test_populate_movies(self):
        """
        Tests if populate_movies command adds movies to different categories
        """
        # Add movies categories
        management.call_command("populate_categories")

        # Add movies to the categories
        management.call_command("populate_movies")

        response = self.client.get("/moviescategories/1")

        self.assertGreater(len(response.data), 0)

    def test_populate_series(self):
        """
        Tests if populate_series command adds different series to the database
        """
        response = self.client.get("/series/")
        self.assertEqual([], response.data)
        # Add series
        management.call_command("populate_series")

        response = self.client.get("/series/")
        self.assertGreater(len(response.data), 0)

    def test_populate_seasons(self):
        """
        Tests if populate_seasons command populate's seasons of a series into the database
        """
        # Add series
        management.call_command("populate_series")

        response = self.client.get("/series/1")

        self.assertEqual([], response.data)

        # Add seasons
        management.call_command("populate_seasons")
        response = self.client.get("/series/1")
        self.assertGreater(len(response.data), 0)

    def test_populate_episodes(self):
        """
        Tests if populate_episodes command adds episodes into different seasons of a series
        """
        # Add series
        management.call_command("populate_series")

        # Add seasons
        management.call_command("populate_seasons")

        response = self.client.get("/episodes/1")

        self.assertEqual([], response.data)

        # Add episodes
        management.call_command("populate_episodes")

        response = self.client.get("/episodes/1")
        self.assertGreater(len(response.data), 0)


