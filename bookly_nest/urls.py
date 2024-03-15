from django.urls import path
from . import views

app_name = "bookly_nest"
urlpatterns = [
    # Home page
    path("", views.index, name="index"),
    path("genres/", views.genres, name="genres"),
    path("genres/<int:genre_id>", views.genre, name="genre"),
    path("new_genre/", views.new_genre, name="new_genre"),
    path("new_book/<int:genre_id>", views.new_book, name="new_book"),
    path("edit_book/<int:book_id>", views.edit_book, name="edit_book"),
    path("delete_book/<int:book_id>", views.delete_book, name="delete_book"),
]
