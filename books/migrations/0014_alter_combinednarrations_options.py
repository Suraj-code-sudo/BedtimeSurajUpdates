# Generated by Django 4.1.8 on 2023-09-19 09:06

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("books", "0013_alter_page_image"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="combinednarrations",
            options={"ordering": ["book", "created_at"]},
        ),
    ]
