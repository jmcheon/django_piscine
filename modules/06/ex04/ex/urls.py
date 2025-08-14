from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path("", views.home_view, name="home"),
    path("signup/", views.signup_view, name="signup"),
    # Django provide views ready to use for login and logout 
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="ex/login.html",
            redirect_authenticated_user=True,  # Redirect user if already logged in 
        ),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(next_page="home"), name="logout"),
    path("tip/<int:pk>/upvote/", views.upvote_view, name="upvote_tip"),
    path("tip/<int:pk>/downvote/", views.downvote_view, name="downvote_tip"),
    path("tip/<int:pk>/delete/", views.delete_tip_view, name="delete_tip"),
    path("api/get-username/", views.get_session_username_view, name="get_username"),
]
