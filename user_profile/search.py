from django.db.models import Q

from user_profile.models import ExtendedUser, UserProfile


def get_user_profile_queryset(query):

    profiles = []
    queries = query.rstrip().lstrip().split(" ")

    if len(queries) > 1:
        profiles = UserProfile.objects.filter(
            Q(first_name__icontains=queries[0]) and Q(last_name__icontains="".join(q+" " for q in queries[1:]).rstrip())
        )
    else:
        users = ExtendedUser.objects.filter(
            Q(username__icontains=query)
        )
        profiles = UserProfile.objects.filter(
            Q(user__in=users) | Q(first_name__icontains=query) | Q(last_name__icontains=query)
        )

    queryset = list(set([profile for profile in profiles]))
    return queryset


