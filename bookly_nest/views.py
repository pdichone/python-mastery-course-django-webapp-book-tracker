from django.http import Http404
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from .forms import GenreForm, BookForm


from .models import Book, Genre


# Create your views here.
def index(request):
    books = Book.objects.all()

    context = {"books": books}
    return render(request, "bookly_nest/index.html", context)


@login_required
def genres(request):
    # genres = Genre.objects.all()
    genres = Genre.objects.filter(owner=request.user)
    context = {"genres": genres}
    return render(request, "bookly_nest/genres.html", context)


@login_required
def genre(request, genre_id):
    genre = Genre.objects.get(id=genre_id)

    if genre.owner != request.user:
        raise Http404
    books = genre.book_set.order_by("-date_added")

    context = {"genre": genre, "books": books}

    return render(request, "bookly_nest/genre.html", context)


@login_required
def new_genre(request):
    if request.method != "POST":
        # No data submitted; create a blank form
        form = GenreForm()
    else:
        # POST data submitted; process data
        form = GenreForm(data=request.POST)

        if form.is_valid():
            # save the form data
            # associate the genre with the current user
            new_genre = form.save(commit=False)
            new_genre.owner = request.user
            new_genre.save()
            return redirect("bookly_nest:genres")

    context = {"form": form}
    return render(request, "bookly_nest/new_genre.html", context)


@login_required
def new_book(request, genre_id):
    genre = Genre.objects.get(id=genre_id)

    if request.method != "POST":
        form = BookForm()

    else:
        form = BookForm(data=request.POST)
        if form.is_valid():
            new_book = form.save(commit=False)
            new_book.genre = genre  # Important - genre-book association!
            new_book.save()

            return redirect("bookly_nest:genre", genre_id=genre_id)
    context = {"genre": genre, "form": form}
    return render(request, "bookly_nest/new_book.html", context)


@login_required
def edit_book(request, book_id):
    book = Book.objects.get(id=book_id)
    genre = book.genre

    if genre.owner != request.user:
        raise Http404

    if request.method != "POST":
        # prefill the form with the current book data
        form = BookForm(instance=book)
    else:
        form = BookForm(instance=book, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("bookly_nest:genre", genre_id=genre.id)

    context = {"book": book, "genre": genre, "form": form}
    return render(request, "bookly_nest/edit_book.html", context)


def delete_book(request, book_id):
    book = Book.objects.get(id=book_id)
    genre = book.genre

    if genre.owner != request.user:
        raise Http404
    if request.method == "POST":
        book.delete()
        return redirect("bookly_nest:genre", genre_id=genre.id)
    elif request.method == "GET":
        context = {"genre": genre, "book": book}
        return render(request, "bookly_nest/delete_book.html", context)
