# Generated by Django 4.1.8 on 2023-09-19 09:05

import books.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("books", "0012_alter_page_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="page",
            name="image",
            field=models.FileField(upload_to=books.models.upload_video),
        ),
    ]
