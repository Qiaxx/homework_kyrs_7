from django.contrib.auth.models import AbstractUser
from django.db import models


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
