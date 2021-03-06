# Generated by Django 3.1 on 2020-08-23 19:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book_functionalities', '0014_remove_bookreview_spoiler'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='author',
            options={'ordering': ['full_name'], 'verbose_name': 'author', 'verbose_name_plural': 'authors'},
        ),
        migrations.AlterModelOptions(
            name='book',
            options={'ordering': ['title', 'author'], 'verbose_name': 'book', 'verbose_name_plural': 'books'},
        ),
        migrations.AlterModelOptions(
            name='bookreview',
            options={'ordering': ['book'], 'verbose_name': 'book review', 'verbose_name_plural': 'book reviews'},
        ),
    ]
