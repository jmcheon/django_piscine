from django.urls import path

from . import views

urlpatterns = [
    path("", views.ex02_view, name="ex02"),
]
