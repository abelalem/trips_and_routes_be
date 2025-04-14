from rest_framework import serializers
from .models import DriverLog, DutyType, GraphGrid

class DriverLogSerializer(serializers.ModelSerializer):
  class Meta:
    model = DriverLog
    fields = '__all__'

class DutyTypeSerializer(serializers.ModelSerializer):
  class Meta:
    model = DutyType
    fields = '__all__'

class GraphGridSerializer(serializers.ModelSerializer):
  class Meta:
    model = GraphGrid
    fields = '__all__'