# Generated by Django 5.1.6 on 2025-03-05 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("advertisements", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="advertisement",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации"),
        ),
    ]
