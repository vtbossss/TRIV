# ndvi/serializers.py
from rest_framework import serializers
from .models import NDVIRecord

class NDVIRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = NDVIRecord
        fields = '__all__'
