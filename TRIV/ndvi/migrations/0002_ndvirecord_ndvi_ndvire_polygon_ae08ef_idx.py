# Generated by Django 4.2.16 on 2024-11-09 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ndvi", "0001_initial"),
    ]

    operations = [
        migrations.AddIndex(
            model_name="ndvirecord",
            index=models.Index(
                fields=["polygon_id", "date"], name="ndvi_ndvire_polygon_ae08ef_idx"
            ),
        ),
    ]