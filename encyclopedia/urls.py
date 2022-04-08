from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("search", views.search, name="search"),
    path("random", views.random, name="random"),
    path("create", views.create, name="create"),
    path("ed/<str:title>", views.edit, name="edit"),
]