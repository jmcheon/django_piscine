from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView

from .models import Article, UserFavouriteArticle


# ex00 View
class ArticleListView(ListView):
    model = Article
    template_name = "ex/article_list.html"
    context_object_name = "articles"


# ex01 Views
class ArticleDetailView(DetailView):
    model = Article
    template_name = "ex/article_detail.html"
    context_object_name = "article"


class PublicationListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = "ex/publications.html"
    context_object_name = "articles"

    def get_queryset(self):
        # This method filters articles to show only those authored by the currently logged-in user.
        return Article.objects.filter(author=self.request.user)


class FavouriteListView(LoginRequiredMixin, ListView):
    model = UserFavouriteArticle
    template_name = "ex/favourites.html"
    context_object_name = "favourites"

    def get_queryset(self):
        # This method filters favourites to show only those belonging to the currently logged-in user.
        return UserFavouriteArticle.objects.filter(user=self.request.user)
