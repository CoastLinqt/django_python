from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import BasedView


app_name = 'blogapp'

urlpatterns = [
    path("", BasedView.as_view(), name="blog"),
]