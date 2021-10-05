from .models import Movie, Review, Rating
from rest_framework import serializers

class FilterReviewListSerializer(serializers.ListSerializer):
    '''Фильтр только для parent комментариев'''
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)

class MovieListSerializer(serializers.ModelSerializer):
    '''Вывод всех фильмов'''

    class Meta:
        model = Movie
        fields = ('title', 'tagline', 'category')

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
