# Generated by Django 3.1 on 2020-08-27 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_functionalities', '0021_auto_20200827_0330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='genres',
            field=models.ManyToManyField(related_name='genre', to='book_functionalities.BookGenre'),
        ),
    ]
