from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView

from jibambe.movies.models import MoviesCategories
from jibambe.movies.serializers import MoviesCategoriesSerializer, SingleCategorySerializer


class MoviesCategoriesList(APIView):
    """
    List All MovieCategories
    """

    def get(self, request):
        movies_categories = MoviesCategories.objects.all()
        serializer = MoviesCategoriesSerializer(movies_categories, many=True)
        return Response(serializer.data)


class MovieCategoryDetails(APIView):
    """
    Show movies contained in this MovieCategory
    """

    def get_object(self, pk):
        try:
            return MoviesCategories.objects.filter(pk=pk)
        except MoviesCategories.DoesNotExist:
            return Http404

    def get(self, request, pk):
        movie_category = self.get_object(pk)
        serializer = SingleCategorySerializer(movie_category, many=True)
        return Response(serializer.data[0]['movies'])


def add_categories(data):
    movies_category = MoviesCategoriesSerializer(data=data)
    if movies_category.is_valid():
        movies_category.save()
        print("Category Saved Successfully")
        return 0
    else:
        print("Error saving category")
        return -1
