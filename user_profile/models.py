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

    profile_pic = models.ImageField(upload_to='profile_picture', blank=True)

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    def __str__(self):
        return f'Profile of {self.first_name} {self.last_name}'



