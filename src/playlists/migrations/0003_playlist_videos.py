# Generated by Django 3.2.4 on 2021-08-03 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0009_alter_video_video_id'),
        ('playlists', '0002_playlist_video'),
    ]

    operations = [
        migrations.AddField(
            model_name='playlist',
            name='videos',
            field=models.ManyToManyField(blank=True, related_name='playlist_item', to='videos.Video'),
        ),
    ]
