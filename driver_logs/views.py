from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from users.models import User, UserType
from .models import DriverLog, Truck, DutyType, GraphGrid
from .serializer import DriverLogSerializer, TruckSerializer, DutyTypeSerializer, GraphGridSerializer

# ========== Drivers Logs ==========

@api_view(['GET'])
def get_drivers_logs(request):
  driver_logs = DriverLog.objects.all()

  return Response(DriverLogSerializer(driver_logs, many = True).data, status = status.HTTP_200_OK)

@api_view(['GET'])
def get_driver_logs(request, user_id):
  try:
    driver_log = DriverLog.objects.get(user_id = user_id)
  except DriverLog.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)

  return Response(DriverLogSerializer(driver_log, many = True), status=status.HTTP_200_OK)

@api_view(['POST'])
def create_driver_log(request):
  driver_log_data = request.data

  try:
    user_type = UserType.objects.get(name = 'Driver')
  except UserType.DoesNotExist:
    return Response("User_Type driver does not exist", status = status.HTTP_404_NOT_FOUND)

  try:
    driver = User.objects.get(id = driver_log_data['driver'], user_type_id = user_type.id)
  except User.DoesNotExist:
    return Response("User with a Driver User_Type for Driver does not exist", status = status.HTTP_404_NOT_FOUND)

  if driver_log_data['co_driver'] is not None:
    try:
      co_driver = User.objects.get(id = driver_log_data['co_driver'], user_type_id = user_type.id)
    except User.DoesNOtExist:
      return Response("User with a Driver User_Type for co_Driver does not exist", status = status.HTTP_404_NOT_FOUND)

  serializedLog = DriverLogSerializer(data = driver_log_data)

  if not serializedLog.is_valid():
    return Response(serializedLog.errors, status=status.HTTP_400_BAD_REQUEST)

  serializedLog.save()

  return Response(serializedLog.data, status=status.HTTP_201_CREATED)

@api_view(['PUT'])
def update_driver_log(request, log_id):
  try:
    driver_log = DriverLog.objects.get(id = log_id)
  except DriverLog.DoesNotExist:
    return Response(status = status.HTTP_404_NOT_FOUND)

  serialized_log = DriverLogSerializer(request.data)

  if not serialized_log.is_valid():
    return Response(serialized_log.errors, status = status.HTTP_400_BAD_REQUEST)

  serialized_log.save()

  return Response(serialized_log.data, status = status.HTTP_200_OK)

# ========== Truck Information ==========
@api_view(['GET'])
def get_truck_info(request, log_id):
  try:
    truck_info = Truck.objects.get(log_id = log_id)
  except DriverLog.DoesNotExist:
    return Response(status = status.HTTP_404_NOT_FOUND)

  return Response(TruckSerializer(truck_info, many = True).data, status = status.HTTP_200_OK)

@api_view(['POST'])
def add_truck_info(request, log_id):
  try:
    driver_log = DriverLog.objects.get(id = log_id)
  except DriverLog.DoesNotExist:
    return Response(status = status.HTTP_404_NOT_FOUND)

  serialized_truck_info = TruckSerializer(request.data)

  if not serialized_truck_info.is_valid():
    return Response(serialized_truck_info.errors, status = status.HTTP_400_BAD_REQUEST)

  serialized_truck_info.save()

  return Response(serialized_truck_info.data, status = status.HTTP_201_CREATED)

@api_view(['PUT'])
def update_truck_info(request, log_id, truck_id):
  try:
    driver_log = DriverLog.objects.get(id = log_id)
  except DriverLog.DoesNotExist:
    return Response(status = status.HTTP_404_NOT_FOUND)

  try:
    truck = Truck.objects.get(id = truck_id)
  except Truck.DoesNotExist:
    return Response(status = status.HTTP_404_NOT_FOUND)

  serialized_truck_info = TruckSerializer(request.data)

  if not serialized_truck_info.is_valid():
    return Response(serialized_truck_info.errors, status = status.HTTP_400_BAD_REQUEST)

  serialized_truck_info.save()

  return Response(serialized_truck_info.data, status = status.HTTP_200_OK)

# ========== Graph Grid Information ==========

@api_view(['GET'])
def get_duty_types(request):
  duty_types = DutyType.objects.all()

  return Response(DutyTypeSerializer(duty_types, many = True).data)

@api_view(['GET'])
def get_graph_grids(request, log_id):
  try:
    driver_log = DriverLog.objects.get(id = log_id)
  except DriverLog.DoesNotExist:
    return Response(status = status.HTTP_404_NOT_FOUND)

  try:
    graph_grids = GraphGrid.objects.get(log_id = log_id)
  except GraphGrid.DoesNotExist:
    return Response(status = status.HTTP_404_NOT_FOUND)

  return Response(GraphGridSerializer(graph_grids, many = True))

@api_view(['POST'])
def add_graph_grid(request, log_id):
  try:
    driver_log = DriverLog.objects.get(id = log_id)
  except DriverLog.DoesNotExist:
    return Response(status = status.HTTP_404_NOT_FOUND)

  serialized_graph_grid = GraphGridSerializer(request.data)

  if not serialized_graph_grid.is_valid():
    return Response(status = status.HTTP_400_BAD_REQUEST)

  serialized_graph_grid.save()

  return Response(serialized_graph_grid.data, status = status.HTTP_201_CREATED)

@api_view(['PUT'])
def update_graph_grid(request, log_id, graph_grid_id):
  try:
    driver_log = DriverLog.objects.get(id = log_id)
  except DriverLog.DoesNotExist:
    return Response(status = status.HTTP_404_NOT_FOUND)

  try:
    graph_grids = GraphGrid.objects.get(log_id = log_id)
  except GraphGrid.DoesNotExist:
    return Response(status = status.HTTP_404_NOT_FOUND)

  serialized_graph_grid = GraphGridSerializer(request.data)

  if not serialized_graph_grid.is_valid():
    return Response(status = status.HTTP_400_BAD_REQUEST)

  serialized_graph_grid.save()

  return Response(serialized_graph_grid.data, status = status.HTTP_200_OK)
