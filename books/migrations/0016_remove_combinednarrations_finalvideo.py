# Generated by Django 4.1.8 on 2023-09-20 08:42

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("books", "0015_alter_combinednarrations_finalvideo_narrator_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="combinednarrations",
            name="finalVideo",
        ),
    ]
