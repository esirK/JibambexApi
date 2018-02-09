from jibambe.movies.serializers import SingleCategorySerializer, SerieSerializer, SeasonSerializer
from jibambe.movies.models import Season, SingleSeries

pb = SingleSeries(name="Prison Break")

s1 = Season(name="Season1", thumbnail="http://", episodes="9", series=pb)

from jibambe.movies.models import Episode, Season

season = Season.objects.first()
episode = Episode(name="Episode 1", thumbnail="http://", source_url="http://", duration="10:20", season=season)
