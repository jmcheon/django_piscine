from django.urls import path
from django.views.generic.base import RedirectView
from django.contrib.auth.views import LoginView
from .views import ArticleListView

urlpatterns = [
    # The home URL must redirect to the articles page.
    path('', RedirectView.as_view(url='/articles/', permanent=True), name='home'),
    
    # The page to display all articles.
    path('articles/', ArticleListView.as_view(), name='articles'),

    path('login/', LoginView.as_view(
        template_name='ex/login.html', 
        redirect_authenticated_user=True
    ), name='login'),
]