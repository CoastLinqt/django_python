from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.http import HttpResponse, HttpRequest
from django.urls import reverse_lazy


def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('/admin')

        return render(request, 'myauth/login.html')

    username = request.POST["username"]
    password = request.POST["password"]

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('/admin/')

    return render(request, 'myauth/login.html', {"error": "Invalid login"})


def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect(reverse("myauth:login"))


class MyLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("myauth:login")


def set_cookie_view(request: HttpRequest) -> HttpResponse:
    response = HttpResponse("Cookie set")
    response.set_cookie("fizz", "buzz", max_age=3600)
    return response


def get_cookie_view(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get("fizz", "default value")
    return HttpResponse(f"Cookie value: {value!r}")


def set_session_view(request: HttpRequest) -> HttpResponse:
    request.session["foobar"] = "spam"
    return HttpResponse("session set!")

def get_session_view(request: HttpRequest) -> HttpResponse:
    value = request.session.get("foobar", "default")
    return HttpResponse(f"session value: {value!r}!")