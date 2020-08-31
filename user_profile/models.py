import os

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.utils.translation import gettext_lazy as _
from django.db import models

from book import settings
from book_functionalities.models import BookRecommendation, BookReview


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

    def __str__(self):
        return f'User: {self.username}'


class UserProfile(models.Model):

    profile_picture = models.ImageField(upload_to='profile_picture', blank=True)
    # profile_picture = ImageCropField(upload_to='profile_picture', blank=True)
    # cropping = ImageRatioField('profile_picture', '500x500')
    # cropping.verbose_name = ''

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    @property
    def displayable_propic(self):
        if self.profile_picture:
            return self.profile_picture.url
        else:
            return settings.STATIC_URL+settings.DEFAULT_USER_IMG

    @property
    def reviews(self):
        return BookReview.objects.filter(user_profile=self)

    @property
    def recommendations(self):
        return BookRecommendation.objects.filter(user_profile=self)

    @property
    def followed_list(self):
        following_relations = UserProfileFollow.objects.filter(follower=self)
        followed_list = list()
        for relation in following_relations:
            followed_list.append(relation.followed)
        return followed_list

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    class Meta:
        verbose_name = 'user profile'
        verbose_name_plural = 'user profiles'
        ordering = ['last_name', 'first_name']

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

    def delete(self, using=None, keep_parents=False):
        res = super(UserProfile, self).delete(using, keep_parents)
        if self.profile_picture.name != "":
            profile_pic_path = settings.MEDIA_ROOT + '/' + self.profile_picture.name
        try:
            os.remove(profile_pic_path)
        except UnboundLocalError:
            pass
        return res


class UserProfileFollow(models.Model):

    follower = models.ForeignKey(
        settings.PROFILE_MODEL,
        on_delete=models.CASCADE,
        related_name='follower',
    )

    followed = models.ForeignKey(
        settings.PROFILE_MODEL,
        on_delete=models.CASCADE,
        related_name='followed',
    )

    creation_datetime = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.follower == self.followed:
            raise ValidationError(_("You can't follow yourself"))
        try:
            UserProfileFollow.objects.get(follower=self.follower, followed=self.followed)
            raise ValidationError(_("You already follow this user"))
        except UserProfileFollow.DoesNotExist:
            pass

    class Meta:
        verbose_name = 'user profile follow'
        verbose_name_plural = 'user profile follows'
        unique_together = ('follower', 'followed')

    def __str__(self):
        return f'{self.follower.user.username} follows {self.followed.user.username}'


class ChatMessage(models.Model):
    text = models.TextField()
    sender = models.ForeignKey(settings.PROFILE_MODEL, on_delete=models.CASCADE, related_name='sended_messages')
    receiver = models.ForeignKey(settings.PROFILE_MODEL, on_delete=models.CASCADE, related_name='received_messages')

    creation_datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'message from {self.sender.user.username} for {self.receiver.user.username}' \
               f' sent at {self.creation_datetime}'

