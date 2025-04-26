from datetime import datetime
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from users.models import User, UserType
from .models import DriverLog, DutyType, GraphGrid
from .serializer import DriverLogSerializer, DutyTypeSerializer, GraphGridSerializer

# ========== Drivers Logs ==========

@api_view(['GET'])
def get_drivers_logs(request):
  driver_logs = DriverLog.objects.all()

  return Response(DriverLogSerializer(driver_logs, many = True).data, status = status.HTTP_200_OK)

@api_view(['GET'])
def get_driver_logs(request, user_id):
  try:
    user_type = UserType.objects.get(name = 'Driver')
  except UserType.DoesNotExist:
    return Response('User_Type driver does not exist', status = status.HTTP_404_NOT_FOUND)

  try:
    user = User.objects.get(id = user_id, user_type_id = user_type.id)
  except User.DoesNotExist:
    return Response("User does not exit", status = status.HTTP_404_NOT_FOUND)

  try:
    driver_logs = DriverLog.objects.filter(driver = user.id)
  except DriverLog.DoesNotExist:
    return Response("No driver logs found", status=status.HTTP_404_NOT_FOUND)

  return Response(DriverLogSerializer(driver_logs, many = True).data, status=status.HTTP_200_OK)

@api_view(['POST'])
def create_driver_log(request):
  driver_log_data = request.data

  try:
    user_type = UserType.objects.get(name = 'Driver')
  except UserType.DoesNotExist:
    return Response("User_Type driver does not exist", status = status.HTTP_404_NOT_FOUND)

  try:
    _ = User.objects.get(id = driver_log_data['driver'], user_type_id = user_type.id)
  except User.DoesNotExist:
    return Response("User with a Driver User_Type for Driver does not exist", status = status.HTTP_404_NOT_FOUND)

  if driver_log_data['co_driver'] is not None:
    try:
      _ = User.objects.get(id = driver_log_data['co_driver'], user_type_id = user_type.id)
    except User.DoesNOtExist:
      return Response("User with a Driver User_Type for co_Driver does not exist", status = status.HTTP_404_NOT_FOUND)

  serializedLog = DriverLogSerializer(data = driver_log_data)

  if not serializedLog.is_valid():
    return Response(serializedLog.errors, status=status.HTTP_400_BAD_REQUEST)

  serializedLog.save()

  return Response(serializedLog.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_driver_log(request, log_id):
  try:
    driver_log = DriverLog.objects.get(id = log_id)
  except DriverLog.DoesNotExist:
    return Response('Driver_Log does not exist', status = status.HTTP_404_NOT_FOUND)

  return Response(DriverLogSerializer(driver_log).data, status = status.HTTP_200_OK)

@api_view(['PUT'])
def update_driver_log(request, log_id):
  driver_log_data = request.data

  try:
    driver_log = DriverLog.objects.get(id = log_id)
  except DriverLog.DoesNotExist:
    return Response(status = status.HTTP_404_NOT_FOUND)

  if driver_log.driver.id.__str__() != driver_log_data['driver']:
    return Response("Can not change driver for driver_log", status = status.HTTP_400_BAD_REQUEST)

  serialized_log = DriverLogSerializer(driver_log, data = request.data)

  if not serialized_log.is_valid():
    return Response(serialized_log.errors, status = status.HTTP_400_BAD_REQUEST)

  serialized_log.save()

  return Response(serialized_log.data, status = status.HTTP_200_OK)

# ========== Graph Grid Information ==========

@api_view(['GET'])
def get_duty_types(request):
  duty_types = DutyType.objects.all()

  return Response(DutyTypeSerializer(duty_types, many = True).data)

@api_view(['GET'])
def get_graph_grids(request, log_id):
  try:
    _ = DriverLog.objects.get(id = log_id)
  except DriverLog.DoesNotExist:
    return Response("Driver_Log Does not exist", status = status.HTTP_404_NOT_FOUND)

  try:
    graph_grids = GraphGrid.objects.filter(driver_log = log_id).order_by("sequence")
  except GraphGrid.DoesNotExist:
    return Response(status = status.HTTP_404_NOT_FOUND)

  return Response(GraphGridSerializer(graph_grids, many = True).data)

@api_view(['POST'])
def add_graph_grid(request, log_id):
  graph_grid_data = request.data

  try:
    driver_log = DriverLog.objects.get(id = log_id)
  except DriverLog.DoesNotExist:
    return Response("Driver_Log does not exist", status = status.HTTP_404_NOT_FOUND)

  try:
    duty_type = DutyType.objects.get(name = graph_grid_data["duty_type"]["name"])
  except DutyType.DoesNotExist:
    return Response("Duty_Type does not exist", status = status.HTTP_404_NOT_FOUND)

  graph_grids = GraphGrid.objects.filter(driver_log = log_id).order_by("sequence")

  if graph_grids.count() > 0 :
    last_index = graph_grids.count() - 1
    new_time = datetime.strptime(graph_grid_data['time'], "%H:%M:%S").time()
    if new_time <= graph_grids[last_index].time :
      return Response("Invalid time value.", status = status.HTTP_400_BAD_REQUEST)

    if graph_grids[last_index].duty_type.name == graph_grid_data['duty_type']['name'] :
      return Response("Invalid duty_type value.", status = status.HTTP_400_BAD_REQUEST)
  elif driver_log.prev_driver_log is not None :
    prev_graph_grids = GraphGrid.objects.filter(driver_log = driver_log.prev_driver_log)
    if prev_graph_grids.count() == 0 :
      return Response("Invalid graph_grid info for prev_driver_log.", status = status.HTTP_400_BAD_REQUEST)
    else :
      last_index = prev_graph_grids.count() - 1
      if prev_graph_grids[last_index].duty_type.name == graph_grid_data['duty_type']['name'] :
        return Response("Invalid duty_type value.", status = status.HTTP_400_BAD_REQUEST)

  graph_grid_dict = {
    "sequence": graph_grids.count() + 1,
    "driver_log": log_id,
    "duty_type": duty_type.id,
    "time": graph_grid_data["time"],
    "remark": graph_grid_data["remark"]
  }

  serialized_graph_grid = GraphGridSerializer(data = graph_grid_dict)

  if not serialized_graph_grid.is_valid():
    return Response(serialized_graph_grid.errors, status = status.HTTP_400_BAD_REQUEST)

  serialized_graph_grid.save()

  return Response(serialized_graph_grid.data, status = status.HTTP_201_CREATED)

@api_view(['PUT'])
def update_graph_grid(request, graph_grid_id):
  graph_grid_data = request.data

  try:
    driver_log = DriverLog.objects.get(id = graph_grid_data['driver_log'])
  except DriverLog.DoesNotExist:
    return Response("Driver_Log for Graph_Grid Does not exist.", status = status.HTTP_400_BAD_REQUEST)

  try:
    graph_grid = GraphGrid.objects.get(id = graph_grid_id)
  except GraphGrid.DoesNotExist:
    return Response("Graph_Grid does not exist", status = status.HTTP_404_NOT_FOUND)

  prev_graph_grids = GraphGrid.objects.filter(sequence = graph_grid.sequence - 1, driver_log = graph_grid.driver_log.id)
  next_graph_grids = GraphGrid.objects.filter(sequence = graph_grid.sequence + 1, driver_log = graph_grid.driver_log.id)

  if prev_graph_grids.count() > 1 and next_graph_grids.count() > 1 :
    return Response("Something wrong with the graph_grid information.", status = status.HTTP_400_BAD_REQUEST)

  # Check for prev time and duty_type
  if prev_graph_grids.count() > 0 :
    if prev_graph_grids[0].time >= datetime.strptime(graph_grid_data["time"], "%H:%M:%S").time() :
      return Response("Invalid time value.", status = status.HTTP_400_BAD_REQUEST)

    if prev_graph_grids[0].duty_type.name == graph_grid_data["duty_type"]["name"] :
      return Response("Invalid duty_type value.", status = status.HTTP_400_BAD_REQUEST)

  # Check for prev duty_type based on prev driver_log
  if driver_log.prev_driver_log is None :
    if graph_grid_data["duty_type"]["name"] == "Off_Duty" :
      return Response("Invalid duty_type value", status = status.HTTP_400_BAD_REQUEST)
  else :
    prev_graph_grids = GraphGrid.objects.filter(driver_log = driver_log.prev_driver_log).order_by("sequence")

    if graph_grid_data["duty_type"]["name"] == prev_graph_grids[prev_graph_grids.count() - 1].duty_type.name :
      return Response("Invalid duty_type value", status = status.HTTP_400_BAD_REQUEST)

  # Check for next time and duty_type
  if next_graph_grids.count() > 0 :
    if next_graph_grids[0].time <= datetime.strptime(graph_grid_data["time"], "%H:%M:%S").time() :
      return Response("Invalid time value.", status = status.HTTP_400_BAD_REQUEST)

    if next_graph_grids[0].duty_type == graph_grid_data["duty_type"]["name"] :
      return Response("Invalid duty_type value.", status = status.HTTP_400_BAD_REQUEST)

  graph_grid_dict = {
    "sequence": graph_grid.sequence,
    "driver_log": graph_grid.driver_log.id,
    "duty_type": graph_grid_data["duty_type"]["name"],
    "time": graph_grid_data["time"],
    "remark": graph_grid_data["remark"]
  }

  serialized_graph_grid = GraphGridSerializer(graph_grid, data = graph_grid_dict)

  if not serialized_graph_grid.is_valid():
    return Response(status = status.HTTP_400_BAD_REQUEST)

  serialized_graph_grid.save()

  return Response(serialized_graph_grid.data, status = status.HTTP_200_OK)
