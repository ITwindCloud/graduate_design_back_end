from ticket.models import User

from django.views.decorators.csrf import csrf_exempt
from captcha.models import CaptchaStore
from django.db.models import Q

from rest_framework.decorators import api_view
from rest_framework.response import Response 

@csrf_exempt
@api_view(["get","post"])
def login(request):
  if request.method == "POST":
    acc = request.POST.get("account")
    password = request.POST.get("password")
    key = request.POST.get("captcha_answer")
    capt = request.POST.get("captcha_input")

    # 需要返回给前端的数据
    is_acc_error = False
    acc_msg = ""

    is_pd_error = False
    pd_msg = ""

    is_capt_error = False
    capt_msg = ""

    result = User.objects.filter(Q(tel=acc)|Q(email=acc))
    if result.count() <= 0:
      is_acc_error = True
      acc_msg = "账号错误或者不存在"
    else:
      user = result[0]

    # if acc not in given_acc:
    #   is_acc_error = True
    #   acc_msg = "账号错误或者不存在"
    
    if not is_acc_error and password != user.password:
      is_pd_error = True
      pd_msg = "密码错误"

    # 检查验证码是否异常
    search = CaptchaStore.objects.filter(hashkey=key)
    if search.count() <= 0:
      is_capt_error = True
      capt_msg = "验证码过期"
    elif search.first().response != capt.lower():
      is_capt_error = True
      capt_msg = "验证码错误"
    
    check_result = not(is_acc_error or is_pd_error or is_capt_error)
    # 当以上三个条件都满足时，跳转至首页
    if check_result:
      return Response({
        "success":True,
        "username": user.name
      })
      # return render(request,"ticket/index.html")
    else:
      data = {
        "is_acc_error":is_acc_error,
        "is_pd_error":is_pd_error,
        "is_capt_error":is_capt_error,
        "acc_msg":acc_msg,
        "pd_msg":pd_msg,
        "capt_msg":capt_msg
      }
      return Response({"data":data})
    
