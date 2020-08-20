import os

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.utils.translation import gettext_lazy as _
from django.db import models

from book import settings


class ExtendedUser(AbstractUser):

    AbstractUser._meta.get_field('email')._unique = True

    terms_of_service_acceptance = models.BooleanField(default=False)
    terms_of_service_acceptance_datetime = models.DateTimeField(auto_now_add=True)

    is_moderator = models.BooleanField(default=False)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = 'extended user'
        verbose_name_plural = 'extended users'

    @property
    def has_profile(self):
        try:
            assert self.profile
            return True
        except ObjectDoesNotExist:
            return False

    def clean(self):
        if not self.terms_of_service_acceptance:
            raise ValidationError(_("To proceed you must accept the terms of service"))


class UserProfile(models.Model):

    profile_picture = models.ImageField(upload_to='profile_picture', blank=True)
    # profile_picture = ImageCropField(upload_to='profile_picture', blank=True)
    # cropping = ImageRatioField('profile_picture', '500x500')
    # cropping.verbose_name = ''

    @property
    def displayable_propic(self):
        if self.profile_picture:
            return self.profile_picture.url
        else:
            return settings.STATIC_URL+settings.DEFAULT_USER_IMG

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    class Meta:
        verbose_name = 'user profile'
        verbose_name_plural = 'user profiles'

    def __str__(self):
        return f'Profile of {self.first_name} {self.last_name}'

    def save(self, *args, **kwargs):
        try:
            old_instance = UserProfile.objects.get(id=self.id)
            if old_instance.profile_picture != self.profile_picture and old_instance.profile_picture.name != "":
                os.remove(settings.MEDIA_ROOT+'/'+old_instance.profile_picture.name)
        except UserProfile.DoesNotExist:
            pass

        return super(UserProfile, self).save(*args, **kwargs)





