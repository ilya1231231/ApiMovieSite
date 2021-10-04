from .views import MovieListView, MovieDetailView, ReviewCreateView, ReviewListView
from django.urls import path, include

urlpatterns = [
    path('movies/', MovieListView.as_view()),
    path('movies/<int:pk>/', MovieDetailView.as_view()),
    path('review/', ReviewCreateView.as_view()),
    path('review-list/', ReviewListView.as_view())

]
