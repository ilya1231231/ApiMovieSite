from .views import (MovieListView,
                    MovieDetailView,
                    ReviewCreateView,
                    ReviewListView,
                    AddStarRatingView,
                    ActorListView,
                    ActorRetriveView
                    )

from django.urls import path, include

urlpatterns = [
    path('movies/', MovieListView.as_view()),
    path('movies/<int:pk>/', MovieDetailView.as_view()),
    path('review/', ReviewCreateView.as_view()),
    path('review-list/', ReviewListView.as_view()),
    path('rating/', AddStarRatingView.as_view()),
    path('actors/', ActorListView.as_view()),
    path('actors/<int:pk>', ActorRetriveView.as_view())

]
