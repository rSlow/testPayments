# Generated by Django 5.0.4 on 2024-04-07 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telegramuser',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Активный'),
        ),
    ]
