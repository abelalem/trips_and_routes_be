from django.http import HttpResponse

def create_user(request):
  return HttpResponse("Create new user endpoint")

def create_intital_user(request):
  return HttpResponse("Create initital user endpoint")