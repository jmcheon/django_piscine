import random
import time

from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import TipForm
from .models import Tip


def home_view(request):
    # Logic for the Tip form
    if request.method == "POST" and request.user.is_authenticated:
        form = TipForm(request.POST)
        if form.is_valid():
            # We don't save all right away in DB to assign user manually
            new_tip = form.save(commit=False)
            new_tip.auteur = request.user
            new_tip.save()
            return redirect("home")
    else:
        form = TipForm()

    # We retreive all the tips to display them from latest to oldest
    all_tips = Tip.objects.all().order_by("-date")

    context = {"tips": all_tips, "tip_form": form}

    # We return the request to the template so that it can access to the session
    return render(request, "ex/home.html", context)


def signup_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()

    return render(request, "ex/signup.html", {"form": form})


@login_required
def upvote_view(request, pk):
    tip = get_object_or_404(Tip, pk=pk)

    # If the user had downvoted, we cancel its downvote
    if request.user in tip.downvotes.all():
        tip.downvotes.remove(request.user)

    # We inverse the upvote if it's already upvoted, we canncel it, otherwise we add it
    if request.user in tip.upvotes.all():
        tip.upvotes.remove(request.user)
    else:
        tip.upvotes.add(request.user)

    return redirect("home")


@login_required
def downvote_view(request, pk):
    tip = get_object_or_404(Tip, pk=pk)

    # If the user previously upvoted, remove the upvote.
    if request.user in tip.upvotes.all():
        tip.upvotes.remove(request.user)

    # Toggle the downvote status
    if request.user in tip.downvotes.all():
        tip.downvotes.remove(request.user)
    else:
        tip.downvotes.add(request.user)

    return redirect("home")


@login_required
def delete_tip_view(request, pk):
    tip = get_object_or_404(Tip, pk=pk)

    # The condition for exercise 04
    can_delete = tip.auteur == request.user or request.user.has_perm("ex.delete_tip")

    if not can_delete:
        return HttpResponseForbidden("You are not allowed to delete this tip.")

    tip.delete()
    return redirect("home")


def get_session_username_view(request):
    """
    Manages the anonymous user session and returns the current username via JSON.
    This view is intended to be called by an AJAX request.
    """
    current_time = time.time()

    # Check if the session is invalid (no username or has expired)
    if "username" not in request.session or current_time > request.session.get(
        "expiry_time", 0
    ):
        # If invalid, create a new session
        new_username = random.choice(settings.RANDOM_USERNAMES)
        request.session["username"] = new_username
        # Set the expiration time to 42 seconds from now
        request.session["expiry_time"] = current_time + 42

    # Prepare the data to be sent as JSON.
    # The key 'username' will be accessible in the JavaScript 'data' object.
    data = {"username": request.session["username"]}

    # Return the data as a JSON response
    return JsonResponse(data)
