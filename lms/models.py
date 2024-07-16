from django.db import models

from config import settings


class Course(models.Model):
    title = models.CharField(max_length=255)
    preview = models.ImageField(
        upload_to="course_previews/previews/", blank=True, null=True
    )
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="владелец",
    )

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
        Course, related_name="course", on_delete=models.CASCADE, blank=True, null=True
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="владелец",
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return self.title


class Subscription(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="владелец",
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, blank=True, null=True, verbose_name="курс"
    )

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    def __str__(self):
        return f"{self.user.email} - {self.course.title}"
