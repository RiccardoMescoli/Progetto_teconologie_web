from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from book import settings


def profile_required(view_func):
    user_has_profile = user_passes_test(
        lambda user: user.has_profile,
        login_url=settings.PROFILE_CREATION_URL
    )
    return login_required(user_has_profile(view_func))


def moderators_only(view_func):
    user_is_moderator = user_passes_test(
        lambda user: user.is_moderator,
        login_url=settings.LOGIN_URL
    )
    return login_required(user_is_moderator(view_func))
