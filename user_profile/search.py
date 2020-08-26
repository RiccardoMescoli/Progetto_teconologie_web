from django.db.models import Q

from book_functionalities.models import Author, BookRecommendation, BookReview


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
