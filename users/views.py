import random, string
from datetime import datetime
from django.contrib.auth.hashers import ( make_password, check_password )
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User, UserType
from .serializers import UserSerializer, UserTypeSerializer

# Users

@api_view(['GET'])
def get_user_types(request):
  userTypes = UserType.objects.all()

  return Response(UserTypeSerializer(userTypes, many = True).data)

@api_view(['GET'])
def get_users(request):
  users = User.objects.filter(is_active = True)

  return Response(UserSerializer(users, many=True).data)

@api_view(['GET'])
def get_user(request, user_id):
  try:
    user = User.objects.get(id = user_id, is_active = True)
  except User.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)

  return Response(UserSerializer(user).data)

@api_view(['POST'])
def create_user(request):
  data = request.data

  try:
    user_type = UserType.objects.get(name = data['user_type'])
  except UserType.DoesNotExist:
    return Response('User_Type does not exist', status=status.HTTP_404_NOT_FOUND)

  user_dict = {
    'user_type_id': user_type.id,
    'user_name': data['user_name'],
    'password': make_password(data['password']),
    'first_name': data['first_name'],
    'middle_name': data['middle_name'],
    'last_name': data['last_name'],
    'email': data['email']
  }

  serializedUser = UserSerializer(data = user_dict)

  if not serializedUser.is_valid():
    return Response(serializedUser.errors, status=status.HTTP_400_BAD_REQUEST)

  serializedUser.save()

  return Response(serializedUser.data, status=status.HTTP_201_CREATED)

@api_view(['PUT'])
def update_user(request, user_id):
  data = request.data

  try:
    user = User.objects.get(id = user_id, is_active = True)
  except User.DoesNotExist:
    return Response('User not found', status=status.HTTP_404_NOT_FOUND)

  try:
    user_type = UserType.objects.get(name = data['user_type'])
  except UserType.DoesNotExist:
    return Response('User_Type not found', status = status.HTTP_404_NOT_FOUND)

  user_dict = {
    'user_type_id': user_type.id,
    'user_name': user.user_name,
    'first_name': data['first_name'],
    'middle_name': data['middle_name'],
    'last_name': data['last_name'],
    'email': data['email']
  }

  serializedUser = UserSerializer(user, data=user_dict)
  if not serializedUser.is_valid():
    return Response(serializedUser.errors, status=status.HTTP_400_BAD_REQUEST)

  serializedUser.save()

  return Response(serializedUser.data)

@api_view(['DELETE'])
def delete_user(request, user_id):
  try:
    user = User.objects.get(id = user_id, is_active = True)
  except User.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)

  user.is_active = False

  user.save()

  return Response(status=status.HTTP_204_NO_CONTENT)

# Auth

@api_view(['POST'])
def sign_in(request):
  data = request.data
  try:
    user = User.objects.get(user_name = data['user_name'])
  except User.DoesNotExist:
    return Response('Invalid user name or password', status = status.HTTP_401_UNAUTHORIZED)

  is_valid_password = check_password(data['password'], user.password)

  if not is_valid_password:
    return Response('Invalid user name or password', status = status.HTTP_401_UNAUTHORIZED)

  user.last_login = datetime.now()
  user_info = {
    'user_name': user.user_name,
    'last_login': user.last_login.__str__(),
    'token': ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=64))
  }

  user.login_token = make_password(user_info['user_name'] + user_info['last_login'] + user_info['token'])

  user.save()

  return Response(user_info, status = status.HTTP_200_OK)

@api_view(['POST'])
def sign_out(request):
  data = request.data

  try:
    user = User.objects.get(user_name = data['user_name'])
  except User.DoesNotExist:
    return Response(status = status.HTTP_401_UNAUTHORIZED)

  is_valid_token = check_password(data['user_name'] + data['last_login'] + data['token'], user.login_token)

  if not is_valid_token:
    return Response(status = status.HTTP_401_UNAUTHORIZED)

  user.login_token = None

  user.save()

  return Response(status = status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def change_password(request):
  data = request.data

  try:
    user = User.objects.get(user_name = data['user_name'])
  except User.DoesNotExist:
    return Response(status = status.HTTP_401_UNAUTHORIZED)

  if user.login_token == None:
    return Response(status = status.HTTP_401_UNAUTHORIZED)

  is_valid_token = check_password(data['user_name'] + data['last_login'] + data['token'], user.login_token)

  if not is_valid_token:
    return Response(status = status.HTTP_401_UNAUTHORIZED)

  is_valid_old_password = check_password(data['old_password'], user.password)

  if not is_valid_old_password:
    return Response(status = status.HTTP_401_UNAUTHORIZED)

  user.password = make_password(data['new_password'])

  user.save()

  return Response(status = status.HTTP_200_OK)