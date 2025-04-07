from rest_framework import serializers
from .models import User, UserType

class UserSerializer(serializers.ModelSerializer): # serializers.HyperlinkedModelSerializer
  class Meta:
    model = User
    fields = ['id', 'user_name', 'first_name', 'middle_name', 'last_name', 'email', 'user_type_id']

class UserTypeSerializer(serializers.ModelSerializer): # serializers.HyperlinkedModelSerializer
  class Meta:
    model = UserType
    fields = '__all__'