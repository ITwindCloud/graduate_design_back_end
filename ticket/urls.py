from django.urls import path
from .views import login,register,index,result,order,user_info_mod
from . import views2
app_name = "ticket"
urlpatterns = [
  # login
  path("login/",login.login,name="login"),
  # register
  path("register/",register.register,name="register"),

  path("get-captcha/",views2.return_captcha,name="captcha"),


  # 输入查询条件时自动进行日期更新
  path("four-dates/", index.get_four_date, name="four-dates"),
  # 查询结果呈现
  path("search-check/",result.check_keyword,name="search-check"),
  path("search-result/", result.search_result,name="search-result"),

  # 预订相关
  path("order/",order.order,name="order"),
  path("order2/",order.order2,name="order2"),
  path("order-submit/",order.order_submit,name="order_submit"),
  path("order-history/",order.history,name="history"),

  # 用户信息
  path("user_info/",user_info_mod.get_user_info,name="get_user_info"),
  path("user_info_mod/",user_info_mod.mod_user_info,name="user_info_mod")

]