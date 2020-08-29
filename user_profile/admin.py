from django.contrib import admin

from user_profile.models import ChatMessage, ExtendedUser, UserProfile, UserProfileFollow

admin.site.register(ExtendedUser)
admin.site.register(UserProfile)
admin.site.register(UserProfileFollow)
admin.site.register(ChatMessage)
