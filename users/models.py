import uuid
from django.db import models

class UserType(models.Model):
  id = models.IntegerField(primary_key=True)
  name = models.CharField(max_length=10, unique=True)

  def __str__(self):
    return self.name

class User(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  user_type_id = models.ForeignKey(UserType, on_delete=models.RESTRICT)
  user_name = models.CharField(max_length=100, unique=True)
  password = models.CharField(max_length=200)
  first_name = models.CharField(max_length=100)
  middle_name = models.CharField(max_length=100)
  last_name = models.CharField(max_length=100)
  email = models.EmailField(unique=True)
  last_login = models.DateTimeField(null=True)
  login_token = models.CharField(max_length=100, null=True)
  is_active = models.BooleanField(default=True)

  def __str__(self):
    return self.user_name

