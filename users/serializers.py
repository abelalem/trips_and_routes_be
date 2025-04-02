from rest_framework import serializers
from .models import User, UserType

class UserSerializer(serializers.ModelSerializer): # serializers.HyperlinkedModelSerializer
  class Meta:
    model = User
    fields = '__all__'

class UserTypeSerializer(serializers.ModelSerializer): # serializers.HyperlinkedModelSerializer
  class Meta:
    model = UserType
    fields = '__all__'