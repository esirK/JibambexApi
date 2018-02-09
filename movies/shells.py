from .models import Season, Series, Episode, Season

pb = Series(name="Prison Break")

s1 = Season(name="Season1", thumbnail="http://", episodes="9", series=pb)

season = Season.objects.first()
episode = Episode(name="Episode 1", thumbnail="http://", source_url="http://", duration="10:20", season=season)
