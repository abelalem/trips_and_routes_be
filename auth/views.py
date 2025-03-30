from django.http import HttpResponse

def login(request):
  return HttpResponse("Login endpoint")

def logout(request):
  return HttpResponse("Logout endpoint")

def change_password(request):
  return HttpResponse("Change password endpoint")