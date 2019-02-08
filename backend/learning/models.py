from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=250)
    bio = models.TextField()


class Course(models.Model):
    authors = models.ManyToManyField(
        Author,
        related_name="courses"
    )

    name = models.CharField(max_length=250)
    description = models.TextField()


class Lesson(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="lessons"
    )

    name = models.CharField(max_length=500)
    index = models.PositiveIntegerField()
    description = models.TextField()
    url = models.URLField()


class Video(models.Model):
    lesson = models.OneToOneField(
        Lesson,
        on_delete=models.CASCADE,
        related_name="video"
    )

    video_id = models.CharField(max_length=250)
    url = models.URLField()
