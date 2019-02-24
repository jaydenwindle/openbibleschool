from django.db import models
from django.contrib.postgres.fields import JSONField


class Author(models.Model):
    name = models.CharField(max_length=250)
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    authors = models.ManyToManyField(
        Author,
        related_name="courses"
    )

    name = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)
    original_url = models.URLField(null=True, blank=True)
    original_host = models.CharField(max_length=250, null=True, blank=True)
    data = JSONField(null=True, blank=True)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="lessons"
    )

    name = models.CharField(max_length=500)
    index = models.PositiveIntegerField(default=0)
    original_url = models.URLField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    recording_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name


class Video(models.Model):
    lesson = models.OneToOneField(
        Lesson,
        on_delete=models.CASCADE,
        related_name="video"
    )

    video_id = models.CharField(max_length=250, null=True, blank=True)
    original_url = models.URLField()

    def __str__(self):
        return self.lesson.name + " (video)"


class Audio(models.Model):
    lesson = models.OneToOneField(
        Lesson,
        on_delete=models.CASCADE,
        related_name="audio"
    )

    audio_id = models.CharField(max_length=250, null=True, blank=True)
    original_url = models.URLField()

    def __str__(self):
        return self.lesson.name + " (audio)"