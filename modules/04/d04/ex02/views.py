import datetime
import os

from django.conf import settings
from django.shortcuts import render

from .forms import TextInputForm


def ex02_view(request):
    form = TextInputForm()
    history = []

    # read existing history
    if os.path.exists(settings.LOG_FILE_PATH):
        with open(settings.LOG_FILE_PATH, "r", encoding="utf-8") as f:
            history = f.readlines()

    if request.method == "POST":
        form = TextInputForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data["text"]
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            entry = f"{timestamp} - {text}\n"

            # add entry to log file
            with open(settings.LOG_FILE_PATH, "a", encoding="utf-8") as f:
                f.write(entry)

            # append entry to displayed history
            history.append(entry)

    return render(request, "ex02/index.html", {"form": form, "history": history})
