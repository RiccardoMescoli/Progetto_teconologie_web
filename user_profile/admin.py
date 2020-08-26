from django.contrib import admin

from user_profile.models import ExtendedUser, UserProfile, UserProfileFollow

admin.site.register(ExtendedUser)
admin.site.register(UserProfile)
admin.site.register(UserProfileFollow)

