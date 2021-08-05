from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.db.models.signals import pre_save

from videos.models import Video

# Create your models here.

class PublishStateOption(models.TextChoices):
        PUBLISH = 'PU', 'Published'
        DRAFT = 'DR', 'Draft'
        UNLSTED = 'UN', 'Unlisted'
        PRIVATE = 'PR', 'Private'

class PlaylistQuerySet(models.QuerySet):
    def published(self):
        now = timezone.now()
        return self.filter(
            state = Video.PlaylistStateOption.PUBLISH,
            publish_timestamp__lte = now
        )

class PlaylistManager(models.Manager):
    def get_queryset(self):
        return PlaylistQuerySet(self.model, using=self._db)

class Playlist(models.Model):
    PlaylistStateOption = PublishStateOption
    title = models.CharField(max_length=220)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    video = models.ForeignKey(Video, null=True, on_delete=models.SET_NULL, related_name='playlist_featured')
    videos = models.ManyToManyField(Video, blank=True, related_name='playlist_item')
    active = models.BooleanField(default=True)
    state = models.CharField(max_length=2, choices=PlaylistStateOption.choices, default=PlaylistStateOption.DRAFT)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated =  models.DateTimeField(auto_now=True)
    publish_timestamp = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)

    objects = PlaylistManager()

    @property
    def is_published(self):
        return self.active

    def save(self, *args, **kwargs):
        if self.state == self.PlaylistStateOption.PUBLISH and self.publish_timestamp is None:
            self.publish_timestamp = timezone.now()
        else:
            self.publish_timestamp = None
        if self.slug == None:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    