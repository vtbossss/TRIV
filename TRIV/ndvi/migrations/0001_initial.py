# Generated by Django 4.2.16 on 2024-11-09 22:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="NDVIRecord",
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
                ("polygon_id", models.CharField(max_length=255)),
                ("date", models.DateField()),
                ("mean_ndvi", models.FloatField()),
                ("min_ndvi", models.FloatField()),
                ("max_ndvi", models.FloatField()),
                ("std_ndvi", models.FloatField()),
            ],
        ),
    ]
