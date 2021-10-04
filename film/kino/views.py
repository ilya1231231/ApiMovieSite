from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import MovieListSerializer, MovieDetailSerializer, ReviewCreateSerializer, ReviewListSerializer
from .models import Movie, Review


class MovieListView(APIView):

    def get(self, request):
        movies = Movie.objects.filter(draft=False)
        serializer = MovieListSerializer(movies, many=True)
        return Response(serializer.data)


class MovieDetailView(APIView):

    def get(self, request, pk):
        movie = Movie.objects.get(id=pk, draft=False)
        serializer = MovieDetailSerializer(movie)
        return Response(serializer.data)


class ReviewCreateView(APIView):
    def post(self, request):
        review = ReviewCreateSerializer(data=request.data)  # Передаем информацию в data
        if review.is_valid():
            review.save()
        return Response(status=201)


class ReviewListView(APIView):
    def get(self, request):
        reviews = Review.objects.all()
        serializer = ReviewListSerializer(reviews, many=True)
        return Response(serializer.data)
