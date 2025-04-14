import uuid
from django.db import models
from users.models import User

class DriverLog(models.Model):

  def truck_info_default():
    return {"truck_number": "", "trailer_numbers": []}

  id = models.UUIDField(primary_key = True, default=uuid.uuid4, editable=False)
  driver = models.ForeignKey(User, on_delete = models.RESTRICT, default = '', related_name="driver")
  date = models.DateField()
  total_miles = models.IntegerField()
  carrier = models.CharField(max_length = 100)
  main_office_address = models.CharField(max_length = 200)
  signature = models.TextField()
  co_driver = models.ForeignKey(User, on_delete = models.RESTRICT, null = True, related_name="co_driver")
  time_zone = models.CharField(max_length = 7)
  document_number = models.CharField(max_length = 100)
  truck_info = models.JSONField("TruckInfo", default = truck_info_default)
  prev_driver_log = models.ForeignKey('self', on_delete = models.RESTRICT, null = True, related_name="previous_driver_log")

  class Meta:
    constraints = [
      models.UniqueConstraint("driver", "date", name = "driver_date_unique_constraint")
    ]

  def __str__(self):
    return  (self.user_id, '_', self.date, '_', self.carrier)

class DutyType(models.Model):
  id = models.IntegerField(primary_key = True)
  name = models.CharField(max_length = 100)

  def _str_(self):
    return self.name

class GraphGrid(models.Model):

  id = models.UUIDField(primary_key = True, default=uuid.uuid4, editable=False)
  sequence = models.PositiveIntegerField(default = 1)
  driver_log = models.ForeignKey(DriverLog, on_delete = models.RESTRICT)
  duty_type = models.ForeignKey(DutyType, on_delete = models.RESTRICT)
  time = models.TimeField()
  remark = models.JSONField("Remark", null = True)

  class Meta:
    constraints = [
      models.UniqueConstraint("sequence", "driver_log", name = "sequence-driver_log-unique_constraint")
    ]

  def __str__(self):
    return (self.sequence, self.driver_log, self.duty_type, self.time)
