from django.shortcuts import render
from django.db import models
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    MovieListSerializer,
    MovieDetailSerializer,
    ReviewCreateSerializer,
    ReviewListSerializer,
    CreateRatingSerializer,
    ActorListSerializer,
    ActorDetailSerializer
    )
from .models import Movie, Review, Actor
from .service import get_client_ip
from rest_framework import generics


class ActorListView(generics.ListAPIView):
    '''Вывод всех актеров или режиссеров'''
    queryset = Actor.objects.all()
    serializer_class = ActorListSerializer

class ActorRetriveView(generics.RetrieveAPIView):
    '''Вывод всех актеров или режиссеров'''
    queryset = Actor.objects.all()
    serializer_class = ActorDetailSerializer


class MovieListView(APIView):

    def get(self, request):
        '''1.смотрим поставил ли юзер с заданным ip оценку 2.Вычисляем среднее значение всех оценок '''
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Count("ratings", filter=models.Q(ratings__ip=get_client_ip(request)))
        ).annotate(
            middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
        )
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


class AddStarRatingView(APIView):
    def post(self, request):
        serializer = CreateRatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(ip=get_client_ip(request))
            return Response(status=201)
        else:
            return Response(status=400)
