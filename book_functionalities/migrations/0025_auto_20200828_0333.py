# Generated by Django 3.1 on 2020-08-28 03:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book_functionalities', '0024_auto_20200827_2242'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookreview',
            options={'ordering': ['book', '-creation_datetime'], 'verbose_name': 'book review', 'verbose_name_plural': 'book reviews'},
        ),
    ]
