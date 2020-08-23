from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from book import settings
from book_functionalities.forms import AuthorCreateForm, AuthorEditForm, BookCreateForm, BookEditForm, \
    BookGenreCreateForm, BookGenreEditForm, BookReviewCreateForm, BookReviewEditForm
from book_functionalities.models import Author, Book, BookGenre, BookReview

from user_profile.decorators import moderators_only, profile_required


# --------AUTHOR--------

class AuthorDetailView(DetailView):
    model = Author
    template_name = 'book_functionalities/author/detail.html'


@method_decorator(moderators_only, name='dispatch')
class AuthorEditView(UpdateView):
    model = Author
    form_class = AuthorEditForm
    template_name = 'book_functionalities/author/edit.html'

    def form_valid(self, form):
        self.success_url = reverse_lazy('book_functionalities:author-detail', args=(self.kwargs.get('pk'),))

        if 'cancel' in self.request.POST:
            return redirect(self.success_url)

        return super(AuthorEditView, self).form_valid(form)


@method_decorator(moderators_only, name='dispatch')
class AuthorDeleteView(DeleteView):
    model = Author
    template_name = 'book_functionalities/author/delete.html'
    success_url = reverse_lazy('homepage')


@method_decorator(moderators_only, name='dispatch')
class AuthorCreateView(CreateView):
    form_class = AuthorCreateForm
    model = Author
    template_name = 'book_functionalities/author/create.html'

    def form_valid(self, form):
        if 'cancel' in self.request.POST:
            return redirect(reverse_lazy('homepage'))

        instance = form.save()
        pk = instance.id
        self.success_url = reverse_lazy('book_functionalities:author-detail', args=(pk,))
        return redirect(self.success_url)


# --------BOOK--------

class BookDetailView(DetailView):
    model = Book
    template_name = 'book_functionalities/book/detail.html'


@method_decorator(moderators_only, name='dispatch')
class BookEditView(UpdateView):
    model = Book
    form_class = BookEditForm
    template_name = 'book_functionalities/book/edit.html'

    def form_valid(self, form):
        self.success_url = reverse_lazy('book_functionalities:book-detail', args=(self.kwargs.get('pk'),))

        if 'cancel' in self.request.POST:
            return redirect(self.success_url)

        return super(BookEditView, self).form_valid(form)


@method_decorator(moderators_only, name='dispatch')
class BookDeleteView(DeleteView):
    model = Book
    template_name = 'book_functionalities/book/delete.html'
    success_url = reverse_lazy('homepage')


@method_decorator(moderators_only, name='dispatch')
class BookCreateView(CreateView):
    form_class = BookCreateForm
    model = Book
    template_name = 'book_functionalities/book/create.html'

    def form_valid(self, form):
        instance = form.save()
        pk = instance.id
        self.success_url = reverse_lazy('book_functionalities:book-detail', args=(pk,))
        return redirect(self.success_url)


# --------BOOK GENRE--------

@method_decorator(moderators_only, name='dispatch')
class BookGenreListView(ListView):
    model = BookGenre
    template_name = 'book_functionalities/book_genre/list.html'


@method_decorator(moderators_only, name='dispatch')
class BookGenreEditView(UpdateView):
    model = BookGenre
    form_class = BookGenreEditForm
    template_name = 'book_functionalities/book_genre/edit.html'
    success_url = reverse_lazy('book_functionalities:book-genre-list')


@method_decorator(moderators_only, name='dispatch')
class BookGenreCreateView(CreateView):
    form_class = BookGenreCreateForm
    model = BookGenre
    template_name = 'book_functionalities/book_genre/create.html'
    success_url = reverse_lazy('book_functionalities:book-genre-list')


@method_decorator(moderators_only, name='dispatch')
class BookGenreDeleteView(DeleteView):
    model = BookGenre
    template_name = 'book_functionalities/book_genre/delete.html'
    success_url = reverse_lazy('book_functionalities:book-genre-list')

# --------BOOK REVIEW--------


@method_decorator(profile_required, name='dispatch')
class BookReviewCreateView(CreateView):
    form_class = BookReviewCreateForm
    model = BookReview
    template_name = 'book_functionalities/book_review/create.html'
    success_url = reverse_lazy('user_profile:own-user-profile-detail')

    def form_valid(self, form):
        profile = self.request.user.profile

        try:
            if BookReview.objects.get(user_profile=profile, book=form.cleaned_data.get('book', None)):
                form.add_error('book', 'You have already reviewed this book')
                return super(BookReviewCreateView, self).form_invalid(form)
        except BookReview.DoesNotExist:
            pass

        instance, _ = BookReview.objects.get_or_create(
            user_profile=profile,
            book=form.cleaned_data.get('book', None),
            rating=form.cleaned_data.get('rating', None)
        )
        instance.title = form.cleaned_data.get('title', '')
        instance.content = form.cleaned_data.get('content', '')
        instance.save()
        return redirect(self.success_url)


@method_decorator(login_required, name='dispatch')
class BookReviewEditView(UpdateView):
    model = BookReview
    form_class = BookReviewEditForm
    template_name = 'book_functionalities/book_review/edit.html'

    def dispatch(self, request, *args, **kwargs):
        review = BookReview.objects.get(id=self.kwargs.get('pk'))
        if request.user.id != review.user_profile.user.id \
                and not (request.user.is_superuser
                         or (request.user.is_moderator and not review.user_profile.user.is_superuser)):
            return redirect(settings.LOGIN_URL)
        self.success_url = reverse_lazy('user_profile:user-profile-detail', args=(review.user_profile.id,))
        return super(BookReviewEditView, self).dispatch(request, args, kwargs)


@method_decorator(login_required, name='dispatch')
class BookReviewDeleteView(DeleteView):
    model = BookReview
    template_name = 'book_functionalities/book_review/delete.html'

    def dispatch(self, request, *args, **kwargs):
        review = BookReview.objects.get(id=self.kwargs.get('pk'))
        if request.user.id != review.user_profile.user.id \
                and not (request.user.is_superuser
                         or (request.user.is_moderator and not review.user_profile.user.is_superuser)):
            return redirect(settings.LOGIN_URL)
        self.success_url = reverse_lazy('user_profile:user-profile-detail', args=(review.user_profile.id,))
        return super(BookReviewDeleteView, self).dispatch(request, args, kwargs)
