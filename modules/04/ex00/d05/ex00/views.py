from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, "index.html", {"title":"Ex00: Markdown Cheatsheet"})
