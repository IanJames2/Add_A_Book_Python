# Generated by Django 2.2.4 on 2021-02-27 23:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('FavBooks3_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='users_who_liked',
            new_name='users_who_favorited',
        ),
    ]