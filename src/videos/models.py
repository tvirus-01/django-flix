from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.db.models.signals import pre_save

# Create your models here.

class PublishStateOption(models.TextChoices):
        PUBLISH = 'PU', 'Published'
        DRAFT = 'DR', 'Draft'
        UNLSTED = 'UN', 'Unlisted'
        PRIVATE = 'PR', 'Private'

class VideoQuerySet(models.QuerySet):
    def published(self):
        now = timezone.now()
        return self.filter(
            state = Video.VideoStateOption.PUBLISH,
            publish_timestamp__lte = now
        )

class VideoManager(models.Manager):
    def get_queryset(self):
        return VideoQuerySet(self.model, using=self._db)

class Video(models.Model):
    VideoStateOption = PublishStateOption
    title = models.CharField(max_length=220)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    video_id = models.CharField(max_length=220, unique=True)
    active = models.BooleanField(default=True)
    state = models.CharField(max_length=2, choices=VideoStateOption.choices, default=VideoStateOption.DRAFT)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated =  models.DateTimeField(auto_now=True)
    publish_timestamp = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)

    objects = VideoManager()

    @property
    def is_published(self):
        return self.active

    def get_playlist_ids(self):
        return list(self.playlist_featured.all().values_list('id', flat=True))

    def save(self, *args, **kwargs):
        if self.state == self.VideoStateOption.PUBLISH and self.publish_timestamp is None:
            self.publish_timestamp = timezone.now()
        else:
            self.publish_timestamp = None
        if self.slug == None:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class VideoAllProxy(Video):
    class Meta:
        proxy = True
        verbose_name = "All Video"
        verbose_name_plural = "All Videos"

class VideoPublishedProxy(Video):
    class Meta:
        proxy = True
        verbose_name = "Published Video"
        verbose_name_plural = "Published Videos"
    