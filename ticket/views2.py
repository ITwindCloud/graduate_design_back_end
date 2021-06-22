# 验证码所需的两个类或者方法
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
# 前后端分离所需的两个引入
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt

# 验证码获取
@csrf_exempt
@api_view(["GET","POST"])
def return_captcha(request):
  print("来了一个验证码的请求")
  if request.method == "GET":
    key = CaptchaStore.generate_key()
    url = captcha_image_url(key)
    data = {
      "key":key,
      "url":url
    }
  else:
    answer = request.POST.get("answer",None)
    input_code = request.POST.get("input_code",None)
    search = CaptchaStore.objects.filter(hashkey=answer)
    if search.count()<1:
      status = 0
      msg = "验证过期"
    else:
      res = search.first().response
      if res == input_code.lower():
        status = 1
        msg = "验证通过"
      else:
        status = 0
        msg = "验证失败"
    data = {
      "status":status,
      "msg":msg
    }

  return Response({"data":data})
