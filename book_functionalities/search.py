from django.db.models import Avg, Count, Q

from book_functionalities.models import Book, BookGenre, BookRecommendation, BookReview


def get_book_review_queryset(title="", author=""):

    reviews = []
    title_query = title.rstrip().lstrip()
    author_query = author.rstrip().lstrip()

    if title_query != "":
        if author_query != "":
            reviews = BookReview.objects.filter(
                Q(book__title__icontains=title_query),
                Q(book__author__full_name__icontains=author_query)
            ).distinct()
        else:
            reviews = BookReview.objects.filter(
                Q(book__title__icontains=title_query)
            ).distinct()
    elif author_query != "":
        reviews = BookReview.objects.filter(
            Q(book__author__full_name__icontains=author_query)
        ).distinct()

    queryset = list(set([review for review in reviews]))
    return queryset


def get_book_recommendation_queryset(title="", author=""):

    recommendations = []
    title_query = title.rstrip().lstrip()
    author_query = author.rstrip().lstrip()

    if title_query != "":
        if author_query != "":
            recommendations = BookRecommendation.objects.filter(
                Q(base_book__title__icontains=title_query),
                Q(base_book__author__full_name__icontains=author_query)
            ).distinct()
        else:
            recommendations = BookRecommendation.objects.filter(
                Q(base_book__title__icontains=title_query)
            ).distinct()
    elif author_query != "":
        recommendations = BookRecommendation.objects.filter(
            Q(base_book__author__full_name__icontains=author_query)
        ).distinct()

    queryset = list(set([recommendation for recommendation in recommendations]))
    return queryset


def get_book_toplist(genre=0, author=""):

    books = []
    try:
        genre_query = int(genre)
    except ValueError:
        return []
    if isinstance(author, str):
        author_query = author.rstrip().lstrip()
    else:
        return []

    if author_query != "":
        if genre_query != 0:
            books = Book.objects.filter(
                Q(author__full_name__icontains=author_query) & Q(genres__in=BookGenre.objects.filter(id=genre_query))
            ).annotate(average=Avg('review__rating')).exclude(average=None).order_by('-average')[:10]
        else:
            books = Book.objects.filter(
                Q(author__full_name__icontains=author_query)
            ).annotate(average=Avg('review__rating')).exclude(average=None).order_by('-average')[:10]

    elif genre_query != 0:
        books = Book.objects.filter(
            Q(genres__in=BookGenre.objects.filter(id=genre_query))
        ).annotate(average=Avg('review__rating')).exclude(average=None).order_by('-average')[:10]

    else:
        books = Book.objects.annotate(average=Avg('review__rating')).exclude(average=None).order_by('-average')[:10]

    queryset = list(set([book for book in books]))
    return queryset


def get_report_list():

    reviews = BookReview.objects.annotate(reports=Count('report')).filter(reports__gt=0).order_by('-reports')[:20]

    queryset = list(set([review for review in reviews]))
    return queryset

