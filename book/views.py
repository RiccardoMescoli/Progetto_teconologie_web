from operator import attrgetter

from django.db.models import Avg, Count, FloatField
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils import timezone

from book_functionalities.models import Book, BookRecommendation, BookReview
from user_profile.decorators import profile_required
from user_profile.models import UserProfile, UserProfileFollow


def homepage(request):

    if request.user.is_authenticated and request.user.has_profile:
        return redirect(reverse_lazy('activity_feed'))

    return render(request, 'home.html')


@profile_required
def activities_feed_view(request):
    context = {}
    datetime_filter = timezone.now() - timezone.timedelta(weeks=1)

    user_profile = request.user.profile
    followed_profiles_ids = UserProfileFollow.objects.filter(follower=user_profile).values('followed')
    followed_profiles = UserProfile.objects.filter(id__in=followed_profiles_ids)

    reviews = BookReview.objects.filter(
        user_profile__in=followed_profiles,
        creation_datetime__gt=datetime_filter
    ).distinct()
    reviews_list = list(set([review for review in reviews]))

    recommendations = BookRecommendation.objects.filter(
        user_profile__in=followed_profiles,
        creation_datetime__gt=datetime_filter
    ).distinct()
    recommendations_list = list(set([recommendation for recommendation in recommendations]))

    context['reviews_list'] = sorted(reviews_list, key=attrgetter('creation_datetime'), reverse=True)
    context['recommendations_list'] = sorted(recommendations_list, key=attrgetter('creation_datetime'), reverse=True)

    return render(request, 'activity_feed.html', context)


@profile_required
def personalized_recommendations_view(request):
    context = {}

    user_profile = request.user.profile
    followed_profiles_ids = UserProfileFollow.objects.filter(follower=user_profile).values('followed')
    followed_profiles = UserProfile.objects.filter(id__in=followed_profiles_ids)

    user_reviewed_books = BookReview.objects.filter(user_profile=user_profile).values_list('book', flat=True)

    if len(user_reviewed_books) > 0 and len(followed_profiles) > 0:
        book_scores = BookRecommendation.objects.filter(
            user_profile__in=followed_profiles,
            base_book__in=user_reviewed_books,
        ).exclude(
            recommended_book__in=user_reviewed_books
         ).select_related('recommended_book').filter(
            recommended_book__review__user_profile__in=followed_profiles
        ).values('recommended_book').annotate(
            score=Count('user_profile', distinct=True, output_field=FloatField()) * (Avg(
                'recommended_book__review__rating', output_field=FloatField())**2)
        ).order_by('-score')[:10].values_list('recommended_book', flat=True)

        books = Book.objects.filter(id__in=book_scores)

        recommended_books_list = list(set([book for book in books]))
        context['results_list'] = sorted(recommended_books_list, key=lambda x: x.avg_rating, reverse=True)
    else:
        context['results_list'] = []

    return render(request, 'personalized_recommendations.html', context)
