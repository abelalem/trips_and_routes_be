from django.urls import path
from .views import *

urlpatterns = [
  path('', get_drivers_logs, name = 'get_drivers_logs'),
  path('<uuid:user_id>/', get_driver_logs, name = 'get_driver_logs'),
  path('create/', create_driver_log, name = 'create_driver_log'),
  path('driver_log/<uuid:log_id>', get_driver_log, name = 'get_driver_log'),
  path('update/<uuid:log_id>', update_driver_log, name = 'update_driver_log'),
  path('graph_grid/duty_types/', get_duty_types, name = 'get_duty_types'),
  path('graph_grid/<uuid:log_id>/', get_graph_grids, name = 'get_graph_grids'),
  path('graph_grid/<uuid:log_id>/add/', add_graph_grid, name = 'add_graph_grid'),
  path('graph_grid/<uuid:graph_grid_id>/update/', update_graph_grid, name = 'update_graph_grid'),
]