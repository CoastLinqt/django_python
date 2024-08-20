from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.views.generic import TemplateView, UpdateView, CreateView, ListView, DetailView
from django.urls import reverse_lazy
from .models import Profile
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.views import View
from .forms import ProfileForm
from django.contrib.auth.mixins import UserPassesTestMixin


class UsersAll(ListView):

    context_object_name = 'users'
    template_name = "myauth/users_all.html"
    queryset = Profile.objects.select_related('user')


class AboutMeView(TemplateView):
    template_name = "myauth/about-me.html"


class UpdateAvatar(UserPassesTestMixin, UpdateView):
    model = Profile
    template_name = "myauth/change_avatar.html"

    form_class = ProfileForm

    def test_func(self):
        if self.request.user.profile.id == self.get_object().id or self.request.user.is_staff:
            return True

    def form_valid(self, form):
        response = super().form_valid(form=form)

        return response

    def get_success_url(self):
        return reverse("myauth:users-all")


class UserDetailsView(DetailView):
    template_name = "myauth/user_detail.html"
    queryset = Profile.objects.all()


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'myauth/register.html'
    success_url = reverse_lazy("myauth:about-me")

    def form_valid(self, form):
        response = super().form_valid(form)

        Profile.objects.create(user=self.object)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")

        user = authenticate(request=self.request, username=username, password=password)
        login(request=self.request, user=user)
        return response


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









@user_passes_test(lambda u: u.is_superuser)
def set_cookie_view(request: HttpRequest) -> HttpResponse:

    response = HttpResponse("Cookie set")
    response.set_cookie("fizz", "buzz", max_age=3600)
    return response


def get_cookie_view(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get("fizz", "default value")
    return HttpResponse(f"Cookie value: {value!r}")


@permission_required("myauth.view_profile", raise_exception=True)
def set_session_view(request: HttpRequest) -> HttpResponse:
    request.session["foobar"] = "spameggs"
    return HttpResponse("session set!")

@login_required
def get_session_view(request: HttpRequest) -> HttpResponse:
    value = request.session.get("foobar", "default")
    return HttpResponse(f"session value: {value!r}!")


class FoobarView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        return JsonResponse({"foo": "bar", "spam": "eggs"})
