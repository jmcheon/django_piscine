from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from django.views.generic.base import RedirectView

from .views import (
    ArticleDetailView,
    ArticleListView,
    FavouriteListView,
    PublicationListView,
)

urlpatterns = [
    # ex00
    # The home URL must redirect to the articles page.
    path("", RedirectView.as_view(url="/articles/", permanent=True), name="home"),
    # The page to display all articles.
    path("articles/", ArticleListView.as_view(), name="articles"),
    path(
        "login/",
        LoginView.as_view(
            template_name="ex/login.html", redirect_authenticated_user=True
        ),
        name="login",
    ),
    # ex01
    # The detail view URL must capture the article's primary key (pk).
    path("article/<int:pk>/", ArticleDetailView.as_view(), name="detail"),
    # The logout view redirects to 'home' on success by default.
    path("logout/", LogoutView.as_view(), name="logout"),
    # Page for the connected user's publications.
    path("publications/", PublicationListView.as_view(), name="publications"),
    # Page for the connected user's favourites.
    path("favourites/", FavouriteListView.as_view(), name="favourites"),
]
