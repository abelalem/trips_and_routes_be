from django.http import HttpResponse

def create_log(request):
  return HttpResponse("Create Driver's Log endpoint")

def update_log(request):
  return HttpResponse("Update Driver's Log endpoint")

def get_log(request):
  return HttpResponse("Get Driver log endpoint")

def get_logs(request):
  return HttpResponse("Get Drivers' logs endpoint")
