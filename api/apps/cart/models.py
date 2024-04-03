from django.db import models

from api.apps.products.models import Product
from api.apps.user.models import User


class UserCart(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь"
    )
    products = models.ManyToManyField(
        to=Product,
        verbose_name="Товары"
    )

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'
