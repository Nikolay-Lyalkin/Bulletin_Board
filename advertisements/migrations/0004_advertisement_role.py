# Generated by Django 5.1.6 on 2025-03-06 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("advertisements", "0003_comment"),
    ]

    operations = [
        migrations.AddField(
            model_name="advertisement",
            name="role",
            field=models.CharField(blank=True, default="user", max_length=5, null=True, verbose_name="Роль"),
        ),
    ]
