from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views


urlpatterns = [

    path(
        "",
        views.home,
        name="home",
    ),

    path(
        "login/",
        views.login_view,
        name="login",
    ),

    path(
        "authority/",
        views.authority,
        name="authority",
    ),

    path(
        "logout/",
        LogoutView.as_view(
            next_page="home",
        ),
        name="logout",
    ),

]