# Generated by Django 3.1 on 2020-08-23 18:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book_functionalities', '0013_remove_bookreview_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookreview',
            name='spoiler',
        ),
    ]
