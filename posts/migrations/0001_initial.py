# Generated by Django 4.1.7 on 2023-05-19 13:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Post",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("updated_on", models.DateTimeField(auto_now=True)),
                ("content", models.TextField()),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="author",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "likes",
                    models.ManyToManyField(
                        blank=True, related_name="likes", to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
            options={
                "ordering": ["-created_on"],
            },
        ),
    ]
