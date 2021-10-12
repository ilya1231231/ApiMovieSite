from .models import Movie, Review, Rating, Actor
from rest_framework import serializers


class ActorListSerializer(serializers.ModelSerializer):
    '''Вывод всех актеров или режиссеров'''
    class Meta:
        model = Actor
        fields = ('id', 'name', 'image')

class ActorDetailSerializer(serializers.ModelSerializer):
    '''Вывод всех актеров или режиссеров'''
    class Meta:
        model = Actor
        fields = '__all__'


class FilterReviewListSerializer(serializers.ListSerializer):
    '''Фильтр только для parent комментариев'''
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)

class MovieListSerializer(serializers.ModelSerializer):
    '''Вывод всех фильмов'''
    rating_user = serializers.BooleanField()
    middle_star = serializers.FloatField()
    class Meta:
        model = Movie
        fields = ('title', 'tagline', 'category', 'rating_user', 'middle_star')

class CreateRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('star', 'movie')

    def create(self, validated_data):   # Validated_data - данные от клиентской стороны
        rating = Rating.objects.update_or_create(
            ip=validated_data.get('ip', None),
            movie=validated_data.get('movie', None),
            defaults={'star': validated_data.get('star')}   # Обновляем только поле star при повторной установке рейтинга
        )
        return rating


class ReviewCreateSerializer(serializers.ModelSerializer):
    '''Создания отзыва'''
    class Meta:
        model = Review
        fields = '__all__'

class RecursiveSerializer(serializers.Serializer):
    '''Рекрусивный(Вложенный) вывод "Child" отзывов'''
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        # ищем всех детей , завязанных на нашем отзыве
        return serializer.data


class ReviewListSerializer(serializers.ModelSerializer):
    '''Отображение Отзыва'''
    child = RecursiveSerializer(many=True)
    class Meta:
        list_serializer_class = FilterReviewListSerializer
        model = Review
        fields = ('name', 'text', 'child')


class MovieDetailSerializer(serializers.ModelSerializer):
    '''Отдельный фильм'''
    '''Добавил сериализатор для актеров и режисссеров'''
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    directors = ActorDetailSerializer( read_only=True, many=True)
    actors = ActorDetailSerializer( read_only=True, many=True)
    genres = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    reviews = ReviewListSerializer(many=True)
    # related name из модели Review на поле movies(по нему можно обратиться к полю Review
    # Используем сериализотор ReviewListSerializer для отображения массива

    class Meta:
        model = Movie
        exclude = ('draft',)
