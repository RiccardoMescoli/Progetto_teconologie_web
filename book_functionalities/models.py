import os
from statistics import mean

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from book import settings


class Author(models.Model):

    portrait = models.ImageField(upload_to='author_portrait', blank=True)

    @property
    def displayable_portrait(self):
        if self.portrait:
            return self.portrait.url
        else:
            return settings.STATIC_URL+settings.DEFAULT_USER_IMG

    full_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    biography = models.TextField()

    class Meta:
        verbose_name = 'author'
        verbose_name_plural = 'authors'

    def __str__(self):
        return f'Author: {self.full_name}'

    def save(self, *args, **kwargs):
        try:
            old_instance = Author.objects.get(id=self.id)
            if old_instance.portrait != self.portrait and old_instance.portrait.name != "":
                portrait_path = settings.MEDIA_ROOT+'/'+old_instance.portrait.name
                try:
                    os.remove(portrait_path)
                except UnboundLocalError:
                    pass
        except Author.DoesNotExist:
            pass
        return super(Author, self).save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        res = super(Author, self).delete(using, keep_parents)
        if self.portrait.name != "":
            portrait_path = settings.MEDIA_ROOT+'/'+self.portrait.name
            try:
                os.remove(portrait_path)
            except UnboundLocalError:
                pass
        return res


class BookGenre(models.Model):
    name = models.CharField(max_length=25, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'book genre'
        verbose_name_plural = 'book genres'

    def __str__(self):
        return f'{self.name}'


class Book(models.Model):

    cover = models.ImageField(upload_to='book_cover', blank=True)

    @property
    def displayable_cover(self):
        if self.cover:
            return self.cover.url
        else:
            return settings.STATIC_URL+settings.DEFAULT_COVER_IMG

    @property
    def avg_rating(self):
        reviews = BookReview.objects.filter(book=self)
        ratings = [review.rating for review in reviews]
        if len(ratings) > 0:
            return round(mean(ratings), 2)
        else:
            return None

    @property
    def ratings_qty(self):
        reviews = BookReview.objects.filter(book=self)
        return len(reviews)

    title = models.CharField(max_length=100)
    release_date = models.DateField()
    synopsis = models.TextField()

    genres = models.ManyToManyField(BookGenre)

    @property
    def genre_name_list(self):
        elements = self.genres.all().values('name')
        names = list()
        for el in elements:
            names.append(el['name'])
        return names

    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'book'
        verbose_name_plural = 'books'

    def __str__(self):
        genre_list_string = "".join([str(genre)+" " for genre in self.genre_name_list])
        return f'"{self.title}" by {self.author.full_name}'+' --Genre: ' + genre_list_string

    def save(self, *args, **kwargs):
        try:
            old_instance = Book.objects.get(id=self.id)
            if old_instance.cover != self.cover and old_instance.cover.name != "":
                cover_path = settings.MEDIA_ROOT+'/'+old_instance.cover.name
            try:
                os.remove(cover_path)
            except UnboundLocalError:
                pass
        except Book.DoesNotExist:
            pass
        return super(Book, self).save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        res = super(Book, self).delete(using, keep_parents)
        if self.cover.name != "":
            cover_path = settings.MEDIA_ROOT+'/'+self.cover.name
            try:
                os.remove(cover_path)
            except UnboundLocalError:
                pass
        return res


class BookReview(models.Model):

    spoiler = models.BooleanField(default=False)
    content = models.CharField(max_length=500)
    rating = models.PositiveSmallIntegerField(MaxValueValidator(10, message="The score can't be higher than 10"))

    user_profile = models.ForeignKey(
        settings.PROFILE_MODEL,
        on_delete=models.CASCADE
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
    )

    creation_datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'book review'
        verbose_name_plural = 'book reviews'
        unique_together = ['user_profile', 'book']

    def __str__(self):
        return f'Review of {self.book.title} by {self.user_profile.user.username}'
