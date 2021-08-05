# Generated by Django 3.2.4 on 2021-08-03 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=220)),
                ('description', models.TextField(blank=True, null=True)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('active', models.BooleanField(default=True)),
                ('state', models.CharField(choices=[('PU', 'Published'), ('DR', 'Draft'), ('UN', 'Unlisted'), ('PR', 'Private')], default='DR', max_length=2)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('publish_timestamp', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]
