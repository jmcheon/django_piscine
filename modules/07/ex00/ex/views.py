from django.views.generic import ListView

from .models import Article


class ArticleListView(ListView):
    model = Article
    template_name = "ex/article_list.html"
    context_object_name = "articles"
