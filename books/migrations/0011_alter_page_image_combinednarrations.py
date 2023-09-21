# Generated by Django 4.1.8 on 2023-09-19 07:38

import books.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("books", "0010_alter_page_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="page",
            name="image",
            field=models.FileField(upload_to=books.models.upload_location),
        ),
        migrations.CreateModel(
            name="CombinedNarrations",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("finalVideo", models.FileField(upload_to="")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "book",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="combined",
                        to="books.book",
                    ),
                ),
                (
                    "narratorName",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="combined", to="books.narration"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="combined",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["book", "pk"],
            },
        ),
    ]