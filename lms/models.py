from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=255)
    preview = models.ImageField(
        upload_to="course_previews/previews/", blank=True, null=True
    )
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.title


class Lesson(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    preview = models.ImageField(
        upload_to="lesson_previews/previews/", blank=True, null=True
    )
    video_url = models.URLField(blank=True, null=True)
    course = models.ForeignKey(
        Course, related_name="lessons", on_delete=models.CASCADE, blank=True, null=True
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return self.title
