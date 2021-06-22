from rest_framework.decorators import api_view
from rest_framework.response import Response 
from ticket.models import User
from django.db.models import Q

@api_view(["GET","POST"])
def get_user_info(request):
  tel = request.GET.get("tel")
  user = User.objects.filter(tel=tel).values()[0]
  return Response({"data":user})

@api_view(["get","post"])
def mod_user_info(request):
  try:
    name = request.GET.get("name","—")
    addr = request.GET.get("addr","—")
    tel = request.GET.get("tel")

    user = User.objects.filter(Q(tel=tel)|Q(email=tel))[0]
    user.name = name
    user.addr = addr
    user.save()
    return Response({"state":"success"})
  except:
    return Response({"state":"failure"})

  


