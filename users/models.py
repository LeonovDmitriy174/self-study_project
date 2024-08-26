from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True, verbose_name="почта", help_text="введите почту", max_length=255
    )
    avatar = models.ImageField(
        upload_to="product/photo",
        blank=True,
        null=True,
        verbose_name="Аватар",
        help_text="Загрузите аватар",
    )
    phone = PhoneNumberField(
        verbose_name="телефон", help_text="введите телефон", blank=True, null=True
    )

    token = models.CharField(
        max_length=255, verbose_name="токен", blank=True, null=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def ad_to_teacher_group(self):
        # Добавляет пользователя в группу преподавателей
        group, _ = Group.objects.get_or_create(name="teacher")
        self.groups.add(group)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
