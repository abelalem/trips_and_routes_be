from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User, UserType
from .serializers import UserSerializer

@api_view(['GET'])
def get_user_types(request):
  userTypes = UserType.objects.all()

  return Response(UserSerializer(userTypes, many = True).data)

@api_view(['GET'])
def get_users(request):
  users = User.objects.all()

  return Response(UserSerializer(users, many=True).data)

@api_view(['GET'])
def get_user(request, user_id):
  try:
    user = User.objects.get(id = user_id)
  except User.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)

  return Response(UserSerializer(user).data)

@api_view(['POST'])
def create_user(request):
  serializedUser = UserSerializer(data = request.data)

  if not serializedUser.is_valid():
    return Response(serializedUser.errors, status=status.HTTP_400_BAD_REQUEST)

  serializedUser.save()

  return Response(serializedUser.data, status=status.HTTP_201_CREATED)

@api_view(['PUT'])
def update_user(request, user_id):
  try:
    user = User.objects.first(id = user_id)
  except User.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)

  serializedUser = UserSerializer(user, data=request.data)
  if not serializedUser.is_valid():
    return Response(serializedUser.error, status=status.HTTP_400_BAD_REQUEST)

  serializedUser.save()

  return Response(serializedUser.data)

@api_view(['DELETE'])
def delete_user(request, user_id):
  try:
    user = User.objects.first(id = user_id)
  except User.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)

  user.delete()

  return Response(status=status.HTTP_204_NO_CONTENT)
