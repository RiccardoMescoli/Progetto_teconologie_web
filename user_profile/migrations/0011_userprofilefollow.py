# Generated by Django 3.1 on 2020-08-24 00:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0010_auto_20200819_2225'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfileFollow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_datetime', models.DateTimeField(auto_now_add=True)),
                ('followed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followed', to='user_profile.userprofile')),
                ('follower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower', to='user_profile.userprofile')),
            ],
            options={
                'verbose_name': 'user profile follow',
                'verbose_name_plural': 'user profile follows',
                'unique_together': {('follower', 'followed')},
            },
        ),
    ]
