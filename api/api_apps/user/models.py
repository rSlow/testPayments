from django.db import models
from django.contrib.auth.models import User


class TimeBasedModel(models.Model):
    class Meta:
        abstract = True
        ordering = ('-created',)

    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')


class TelegramUser(TimeBasedModel):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='Пользователь'
    )
    telegram_id = models.BigIntegerField(
        unique=True,
        db_index=True,
        verbose_name='ID Telegram',
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активный"
    )

    def __str__(self):
        return f'{self.telegram_id}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
