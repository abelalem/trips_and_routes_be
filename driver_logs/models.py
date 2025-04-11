import uuid
from django.db import models
from users.models import User

class DriverLog(models.Model):
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

  class Meta:
    constraints = [
      models.UniqueConstraint("date", "driver", name = "date_driver_unique_constraint")
    ]

  def __str__(self):
    return  (self.user_id, '_', self.date, '_', self.carrier)

class Truck(models.Model):
  id = models.UUIDField(primary_key = True, default=uuid.uuid4, editable=False)
  log_id = models.ForeignKey(DriverLog, on_delete = models.RESTRICT)
  truck_number = models.CharField(max_length = 100)
  trailer_number = models.CharField(max_length = 100)

  def __str__(self):
    return (self.log_id, '_', self.truck_number, '_', self.trailer_number)

class DutyType(models.Model):
  id = models.IntegerField(primary_key = True)
  name = models.CharField(max_length = 100)

  def _str_(self):
    return self.name

class GraphGrid(models.Model):
  id = models.UUIDField(primary_key = True, default=uuid.uuid4, editable=False)
  log_id = models.ForeignKey(DriverLog, on_delete = models.RESTRICT)
  duty_type_id = models.ForeignKey(DutyType, on_delete = models.RESTRICT)
  time = models.TimeField()
  remark = models.CharField(max_length = 200)

  def __str__(self):
    return (self.log_id, self.duty_type_id, self.time, self.remark)
