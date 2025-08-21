from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search/", views.search, name="search"),
    path("blogview/", views.blogview, name="blogview"),
    path("<slug:slug>/", views.post, name="post"),
]