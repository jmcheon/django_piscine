from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.shortcuts import render


def account_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # User has been authenticated, log them in
            user = form.get_user()
            login(request, user)
            return JsonResponse({"success": True})
        else:
            # Form is not valid, return errors
            # The status code 400 indicates a bad request from the client
            return JsonResponse({"success": False, "errors": form.errors}, status=400)

    # For GET request, just display the page with an empty form
    form = AuthenticationForm()
    return render(request, "account/account.html", {"form": form})


def logout_view(request):
    if request.method == "POST":
        logout(request)
        return JsonResponse({"success": True})

    # If not a POST request, it's a bad request
    return JsonResponse({"success": False}, status=400)
