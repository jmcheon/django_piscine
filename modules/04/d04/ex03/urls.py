from django.urls import path

from .views import gradient_table

urlpatterns = [path("", gradient_table, name="gradient_table")]
