from django.urls import path
from .views import (login_view,
                    set_cookie_view,
                    get_cookie_view,
                    set_session_view,
                    get_session_view,
                    logout_view,
                    MyLogoutView,
                    AboutMeView,
                    RegisterView,
                    FoobarView,)
from django.contrib.auth.views import LoginView

app_name = "myauth"

urlpatterns = [

    # path("login/", login_view, name="login"),
    path('register/', RegisterView.as_view(), name='register'),
    path('about-me/', AboutMeView.as_view(), name='about-me'),
    path(
        "login/",
        LoginView.as_view(
            template_name="myauth/login.html",
            redirect_authenticated_user=True,
        ),
        name="login"
    ),
    path("logout/", MyLogoutView.as_view(), name="logout"),
    path("cookie/get/", get_cookie_view, name="get_cookie"),
    path("cookie/set/", set_cookie_view, name="set_cookie"),
    path("session/get/", get_session_view, name="get_session"),
    path("session/set/", set_session_view, name="set_session"),
    path("foo-bar", FoobarView.as_view(), name="foo-bar")
]