from rest_framework.response import Response
from rest_framework.views import APIView

from jibambe.movies.models import MoviesCategories
from jibambe.movies.serializers import MoviesCategoriesSerializer


class MoviesCategoriesList(APIView):
    """
    List All MovieCategories together with their movies
    """
    def get(self, request):
        movies_categories = MoviesCategories.objects.all()
        serializer = MoviesCategoriesSerializer(movies_categories, many=True)
        return Response(serializer.data)
