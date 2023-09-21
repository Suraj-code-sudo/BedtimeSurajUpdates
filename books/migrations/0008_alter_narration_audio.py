# Generated by Django 4.1.8 on 2023-07-27 13:11

import books.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("books", "0007_rename_recording_name_recording_narrator_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="narration",
            name="audio",
            field=models.FileField(upload_to=books.models.upload_location),
        ),
    ]