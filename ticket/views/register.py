# from django.shortcuts import render,redirect
# from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..models import User

@csrf_exempt
@api_view(["GET","POST"])
def register(request):
  if request.method == "GET":
    return render(request,"ticket/register.html")
  else:
    print("发来了请求")
    is_tel_error = False
    tel_error = ""
    is_email_error = False
    email_error = ""

    tel = request.POST.get("tel")
    email = request.POST.get("email")
    if request.POST.get("gender")=="female":
      gender=False
    else:
      gender=True

    if User.objects.filter(tel=tel).count()>0:
      is_tel_error = True
      tel_error = "此电话号码已经被注册"
    if User.objects.filter(email=email).count()>0:
      is_email_error = True
      email_error = "此邮箱已经被绑定到其他账号上"
    
    if not is_tel_error and not is_email_error:
      User.objects.create(name=request.POST["name"],tel=tel,email=email,addr=request.POST["abbr"],
              password=request.POST["password"],gender=gender)
      # return redirect("ticket:login")
      return Response({"data":{"state":True}})
    else:
      print("电话和邮箱冲突")
      data = {
        "is_tel_error":is_tel_error,
        "is_email_error":is_email_error,
        "tel_error":tel_error,
        "email_error":email_error,
        "state":False
      }
      return Response({"data":data})