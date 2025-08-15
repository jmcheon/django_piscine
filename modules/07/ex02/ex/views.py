from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic import CreateView, DetailView, ListView

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


# ex02
class AnonymousRequiredMixin:
    """
    Mixin that redirects an authenticated user to the home page.
    """

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # Redirect to the URL defined in LOGIN_REDIRECT_URL
            return redirect(settings.LOGIN_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)


class RegisterView(AnonymousRequiredMixin, generic.CreateView):
    form_class = UserCreationForm
    # reverse_lazy is used because the URLs are not loaded when the file is imported.
    success_url = reverse_lazy("login")
    template_name = "ex/register.html"


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    # The 'author' field is intentionally excluded.
    fields = ["title", "synopsis", "content"]
    template_name = "ex/publish.html"
    success_url = reverse_lazy(
        "publications"
    )  # Redirect to the user's publications list

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        # We assign the current user to the article's author field.
        form.instance.author = self.request.user
        return super().form_valid(form)


class AddFavouriteView(LoginRequiredMixin, CreateView):
    model = UserFavouriteArticle
    fields = []  # No fields are needed from the form itself

    def form_valid(self, form):
        try:
            # We get the article's pk from the URL
            article_id = self.kwargs.get("pk")
            article = Article.objects.get(pk=article_id)
            form.instance.article = article
            form.instance.user = self.request.user
            return super().form_valid(form)
        except IntegrityError:
            # This handles cases where the user tries to favourite an article they have already favourited.
            return redirect("detail", pk=self.kwargs.get("pk"))

    def get_success_url(self):
        # Redirect back to the detail page of the article just favourited.
        return reverse("detail", kwargs={"pk": self.kwargs.get("pk")})
