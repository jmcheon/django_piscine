from django.urls import path

from . import views

urlpatterns = [
    path("", views.django_page, name="home"),
    path("django/", views.django_page, name="django_page"),
    path("display/", views.display_page, name="display_page"),
    path("templates/", views.templates_page, name="templates_page"),
]
