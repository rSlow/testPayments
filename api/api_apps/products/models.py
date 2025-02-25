from pathlib import Path

from django.db import models


class Category(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name="Категория"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ["name"]


class SubCategory(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name="Подкатегория"
    )
    category = models.ForeignKey(
        to=Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        verbose_name="Категория",
        related_name="subcategories"
    )

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'
        ordering = ["name"]

    def __str__(self):
        return self.name


def get_photo_path(product: "Product", filename: str):
    return (Path("products") / product.subcategory.category.name / product.subcategory.name / filename).as_posix()


class Product(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name="Название"
    )
    description = models.TextField(
        verbose_name="Описание",
        null=True
    )
    photo = models.ImageField(
        upload_to=get_photo_path,
        verbose_name="Изображение"
    )
    subcategory = models.ForeignKey(
        to=SubCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        verbose_name="Подкатегория",
        related_name="products"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
