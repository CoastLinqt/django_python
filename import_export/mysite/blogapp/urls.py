from django.urls import path, include
from .views import BasedView, ArticleDetailView, LatestArticlesFeed


app_name = 'blogapp'

urlpatterns = [
    path("article/", BasedView.as_view(), name="blog"),
    path("article/<int:pk>/", ArticleDetailView.as_view(), name="article"),
    path("article/latest/feed", LatestArticlesFeed(), name="articles-feed")
]