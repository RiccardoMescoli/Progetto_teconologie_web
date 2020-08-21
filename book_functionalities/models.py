import os

from django.core.validators import MaxValueValidator
from django.db import models

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
                os.remove(settings.MEDIA_ROOT+'/'+old_instance.portrait.name)
        except Author.DoesNotExist:
            pass

        return super(Author, self).save(*args, **kwargs)


class BookGenre(models.Model):
    name = models.CharField(max_length=25)

    class Meta:
        ordering = ['name']


class Book(models.Model):

    cover = models.ImageField(upload_to='book_cover', blank=True)

    @property
    def displayable_cover(self):
        if self.cover:
            return self.cover.url
        else:
            return settings.STATIC_URL+settings.DEFAULT_COVER_IMG

    title = models.CharField(max_length=100)
    release_date = models.DateField()
    synopsis = models.TextField()

    genre = models.ManyToManyField(BookGenre)

    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'book'
        verbose_name_plural = 'books'

    def __str__(self):
        return f'{self.title} by {self.author.full_name}'


class BookReview(models.Model):

    title = models.CharField(max_length=50)
    content = models.TextField()
    score = models.PositiveSmallIntegerField(MaxValueValidator(10, message="The score can't be higher tha 10"))

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE
    )

