# Generated by Django 4.1.8 on 2023-06-25 14:13

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
            name="Book",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200)),
                ("description", models.TextField()),
            ],
            options={
                "ordering": ["title"],
            },
        ),
        migrations.CreateModel(
            name="CustomizedBook",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("book", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="books.book")),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="customized_books",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Page",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("page_number", models.PositiveIntegerField()),
                ("label", models.CharField(max_length=10)),
                ("image", models.ImageField(upload_to="")),
                (
                    "book",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="pages", to="books.book"
                    ),
                ),
            ],
            options={
                "ordering": ["book", "page_number"],
            },
        ),
        migrations.CreateModel(
            name="Narration",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("narrator_name", models.CharField(max_length=200)),
                ("timestamps", models.JSONField()),
                ("audio", models.FileField(upload_to="")),
                ("public", models.BooleanField(default=False)),
                (
                    "book",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="narrations", to="books.book"
                    ),
                ),
                (
                    "customized_book",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="narrations",
                        to="books.customizedbook",
                    ),
                ),
            ],
        ),
    ]
