from django.urls import path
from .views import *

urlpatterns = [
  path('', get_drivers_logs, name = 'get_drivers_logs'),
  path('<uuid:user_id>/', get_driver_logs, name = 'get_driver_logs'),
  path('create/', create_driver_log, name = 'create_driver_log'),
  path('update/', update_driver_log, name = 'update_driver_log'),
  path('truck/<uuid:log_id>/', get_truck_info, name = 'get_truck_information'),
  path('truck/<uuid:log_id>/add/', add_truck_info, name = 'add_truck_information'),
  path('truck/<uuid:log_id>/update/', update_truck_info, name = 'update_truck_information'),
  path('graph_grid/duty_types/', get_duty_types, name = 'get_duty_types'),
  path('graph_grid/<uuid:log_id>/', get_graph_grids, name = 'get_graph_grids'),
  path('graph_grid/<uuid:log_id>/add/', add_graph_grid, name = 'add_graph_grid'),
  path('graph_grid/<uuid:log_id>/update/', update_graph_grid, name = 'update_graph_grid'),
]