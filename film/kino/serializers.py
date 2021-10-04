from .models import Movie, Review
from rest_framework import serializers


class MovieListSerializer(serializers.ModelSerializer):
    '''Вывод всех фильмов'''

    class Meta:
        model = Movie
        fields = ('title', 'tagline', 'category')


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class ReviewListSerializer(serializers.ModelSerializer):
    '''Отображение Отзыва'''
    class Meta:
        model = Review
        fields = ('name', 'text', 'parent')


class MovieDetailSerializer(serializers.ModelSerializer):
    '''Отдельный фильм'''
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    directors = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    actors = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    genres = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    reviews = ReviewListSerializer(many=True)
    # related name из модели Review на поле movies(по нему можно обратиться к полю Review
    # Используем сериализотор ReviewListSerializer для отображения массива

    class Meta:
        model = Movie
        exclude = ('draft',)
