from django.db import models

# Create your models here.
# ndvi/models.py
from django.contrib.gis.db import models

class NDVIRecord(models.Model):
    polygon_id = models.CharField(max_length=255)
    date = models.DateField()
    mean_ndvi = models.FloatField()
    min_ndvi = models.FloatField()
    max_ndvi = models.FloatField()
    std_ndvi = models.FloatField()

    class Meta:
        indexes = [
            models.Index(fields=['polygon_id', 'date']),
        ]

    def __str__(self):
        return f"NDVI Record {self.polygon_id} on {self.date}"
