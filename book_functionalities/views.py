from operator import attrgetter

from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.shortcuts import redirect, render

from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from book import settings
from book_functionalities.forms import AuthorCreateForm, AuthorEditForm, BookCreateForm, BookEditForm, \
    BookGenreCreateForm, BookGenreEditForm, BookRecommendationCreateForm, BookReviewCreateForm, BookReviewEditForm
from book_functionalities.models import Author, Book, BookGenre, BookRecommendation, BookReview, ReviewReport

from user_profile.decorators import moderators_only, profile_required

from book_functionalities.search import get_book_recommendation_queryset, get_book_review_queryset, get_book_toplist, \
    get_report_list


# ---------------- AUTHOR -----------------


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


# ---------------- BOOK ----------------

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


# -------------- BOOK GENRE -------------

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


# --------------- BOOK REVIEW ---------------


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
        if request.user.id != review.user_profile.user.id:
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


# ----------------- BOOK RECOMMENDATION -------------------

@method_decorator(profile_required, name='dispatch')
class BookRecommendationCreateView(CreateView):
    form_class = BookRecommendationCreateForm
    model = BookRecommendation
    template_name = 'book_functionalities/book_recommendation/create.html'
    success_url = reverse_lazy('user_profile:own-user-profile-detail')

    def form_valid(self, form):
        profile = self.request.user.profile

        if form.cleaned_data.get('base_book', None) == form.cleaned_data.get('recommended_book', None):
            form.add_error('recommended_book', "The two books can't be the same")
            return super(BookRecommendationCreateView, self).form_invalid(form)

        try:
            if BookRecommendation.objects.get(
                    user_profile=profile,
                    base_book=form.cleaned_data.get('base_book', None),
                    recommended_book=form.cleaned_data.get('recommended_book', None)
            ):
                form.add_error('recommended_book', 'You have already made this suggestion')
                return super(BookRecommendationCreateView, self).form_invalid(form)
        except BookRecommendation.DoesNotExist:
            pass

        instance, _ = BookRecommendation.objects.get_or_create(
            user_profile=profile,
            base_book=form.cleaned_data.get('base_book', None),
            recommended_book=form.cleaned_data.get('recommended_book', None)
        )
        instance.save()
        return redirect(self.success_url)


@method_decorator(profile_required, name='dispatch')
class BookRecommendationDeleteView(DeleteView):
    form_class = BookRecommendationCreateForm
    model = BookRecommendation
    template_name = 'book_functionalities/book_recommendation/delete.html'
    success_url = reverse_lazy('user_profile:own-user-profile-detail')

    def dispatch(self, request, *args, **kwargs):
        recommendation = BookRecommendation.objects.get(id=self.kwargs.get('pk'))
        if request.user.id != recommendation.user_profile.user.id:
            return redirect(settings.LOGIN_URL)

        return super(BookRecommendationDeleteView, self).dispatch(request, args, kwargs)

# ------------ REVIEW REPORT -----------


@moderators_only
def review_report_clear(request, **kwargs):

    context = {}

    try:
        review = BookReview.objects.get(pk=kwargs.get('pk', ''))
    except BookReview.DoesNotExist:
        return Http404('Review not found')

    if request.POST:
        ReviewReport.objects.filter(review=review).delete()
        return redirect(reverse_lazy('book_functionalities:report-list'))

    context['review'] = review

    return render(request, 'book_functionalities/review_report/clear.html', context)


# ------------ SEARCH PAGES ------------

def book_review_search_view(request):

    context = {}

    if request.GET:
        title = request.GET.get('title', '')
        author = request.GET.get('author', '')
        context['title_query'] = title
        context['author_query'] = author

        results_list = sorted(get_book_review_queryset(title, author), key=attrgetter('book.title'), reverse=False)
        context['results_list'] = results_list

    return render(request, 'book_functionalities/search_pages/book_review/search.html', context)


def book_recommendation_search_view(request):

    context = {}

    if request.GET:
        title = request.GET.get('title', '')
        author = request.GET.get('author', '')
        context['title_query'] = title
        context['author_query'] = author

        results_list = sorted(get_book_recommendation_queryset(title, author),
                              key=attrgetter('base_book.title'),
                              reverse=False
                              )
        context['results_list'] = results_list

    return render(request, 'book_functionalities/search_pages/book_recommendation/search.html', context)


def book_top_list_view(request):

    context = {}
    genre_list = BookGenre.objects.all()
    genre_query = 0
    author = ""
    if request.GET:
        genre_query = request.GET.get('genre', 0)
        author = request.GET.get('author', '')
        context['genre_query'] = genre_query
        context['author_query'] = author

    results_list = sorted(get_book_toplist(genre_query, author), key=attrgetter('average'), reverse=True)
    context['results_list'] = results_list
    context['genre_list'] = genre_list

    return render(request, 'book_functionalities/search_pages/book/top_list.html', context)


@moderators_only
def report_list_view(request):
    context = {}
    result_list = sorted(get_report_list(), key=attrgetter('reports'), reverse=True)
    context['results_list'] = result_list

    return render(request, 'book_functionalities/search_pages/review_report/most_reported_list.html', context)


# --------------- AJAX -----------------

@login_required
def ajax_report_review(request):
    reported_by = request.user

    try:
        review = BookReview.objects.get(pk=request.GET.get('review', False))
    except BookReview.DoesNotExist:
        return JsonResponse(
            {
                'already_reported': False,
                'is_success': False
            }
        )

    try:
        ReviewReport.objects.get(user=reported_by, review=review)
        return JsonResponse(
            {
                'already_reported': True,
                'is_success': False
            }
        )
    except ReviewReport.DoesNotExist:
        instance, _ = ReviewReport.objects.get_or_create(user=reported_by, review=review)
        instance.save()

        return JsonResponse(
            {
                'already_reported': False,
                'is_success': True
            }
        )

