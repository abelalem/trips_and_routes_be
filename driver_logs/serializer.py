from rest_framework import serializers
from users.serializers import UserSerializer
from .models import DriverLog, DutyType, GraphGrid

class DriverLogSerializer(serializers.ModelSerializer):
  class Meta:
    model = DriverLog
    fields = (
      "id",
      "driver",
      "date",
      "total_miles",
      "carrier",
      "main_office_address",
      "signature",
      "co_driver",
      "time_zone",
      "document_number",
      "truck_info",
      "prev_driver_log"
    )

class DutyTypeSerializer(serializers.ModelSerializer):
  class Meta:
    model = DutyType
    fields = (
      "id",
      "name"
    )

class GraphGridSerializer(serializers.ModelSerializer):
  duty_type = DutyTypeSerializer(read_only = True)
  class Meta:
    model = GraphGrid
    fields = (
      "id",
      "sequence",
      "driver_log",
      "duty_type",
      "time",
      "remark"
    )