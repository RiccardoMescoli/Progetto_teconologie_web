from django.contrib import admin


from user_profile.models import ExtendedUser, UserProfile

admin.site.register(ExtendedUser)
admin.site.register(UserProfile)

