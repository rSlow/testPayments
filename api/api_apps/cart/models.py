from django.core.validators import MinValueValidator
from django.db import models

from api_apps.products.models import Product
from api_apps.user.models import TelegramUser


class UserCart(models.Model):
    user = models.OneToOneField(
        to=TelegramUser,
        on_delete=models.CASCADE,
        verbose_name="Пользователь"
    )

    def __str__(self):
        return f"Корзина пользователя ID {self.user.telegram_id}"

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'


class ProductInCart(models.Model):
    product = models.OneToOneField(
        to=Product,
        on_delete=models.CASCADE,
        verbose_name="Товар"
    )
    cart = models.ForeignKey(
        to=UserCart,
        verbose_name="Корзина пользователя",
        on_delete=models.CASCADE,
        related_name="products"
    )
    count = models.IntegerField(
        verbose_name="Количество",
        validators=[MinValueValidator(1)]
    )

    def __str__(self):
        return str(self.product)

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'
