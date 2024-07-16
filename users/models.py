from django.contrib.auth.models import AbstractUser
from django.db import models

from lms.models import Course, Lesson


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="почта")
    phone = models.CharField(
        max_length=35,
        blank=True,
        null=True,
        verbose_name="телефон",
        help_text="Введите номер телефона",
    )
    town = models.CharField(
        max_length=35,
        blank=True,
        null=True,
        verbose_name="город",
        help_text="Добавьте свой город",
    )
    photo = models.ImageField(
        upload_to="users/photo/",
        blank=True,
        null=True,
        verbose_name="фото",
        help_text="Добавьте свое фото",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


class Payments(models.Model):
    PAYMENT_METHODS = [("cash", "Cash"), ("bank_transfer", "Bank Transfer")]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="пользователь",
        blank=True,
        null=True,
    )
    date_payment = models.DateTimeField(auto_now_add=True)
    paid_course = models.ForeignKey(
        Course,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="course_payments",
    )
    paid_lesson = models.ForeignKey(
        Lesson,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="lesson_payments",
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=15, choices=PAYMENT_METHODS)

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"

    def __str__(self):
        return f"{self.user} - {self.amount} ({self.date_payment})"
