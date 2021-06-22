from rest_framework.decorators import api_view
from rest_framework.response import Response
from ticket.models import AoyouTicket
import datetime
import re
from ticket.models import User
from django.db.models import Q
from sklearn.externals import joblib
from sklearn.ensemble import RandomForestClassifier

def translate_timedelta(time):
  return datetime.timedelta(hours=time.hour,minutes=time.minute)
def compute_duration(time1,time2):
  return translate_timedelta(time2) - translate_timedelta(time1)

def chinese_time(t):
  hour = int(re.findall(r'(\d{1,2}):',t)[0])
  minute = int(re.findall(r'(\d{1,2}):',t)[1])
  return str(hour) + "小时" + str(minute) + "分钟"
def chinese_date(d):
  month = d.month
  day = d.day
  return str(month) + "月" + str(day) + "日"


def get_one_ticket_info(id,acc):
  ticket = AoyouTicket.objects.filter(id=id).values("id","date","start_time","end_time","start_airport__name",\
        "end_airport__name","airline","catagory","price","discount")
  duration = compute_duration(ticket[0]["start_time"],ticket[0]["end_time"])

  user = User.objects.filter(Q(tel=acc)|Q(email=acc)).values("id","name","tel","money")
  data = {
    "ticket": ticket[0],
    "duration": chinese_time(str(duration)),
    "user_info": user[0],
    "date": chinese_date(ticket[0]["date"])
  }
  return data

@api_view(["get","post"])
def order(request):
  id = request.GET.get("id",1891)
  acc = request.GET.get("account","13164137913")
  data = get_one_ticket_info(id,acc)

  model = joblib.load("rfc.joblib")

  # traits = ["id","price","price_rate","day_in_month","day_in_week","is_weekday"]
  # 整理需要训练的数据
  user_id = data["user_info"]["id"]
  price = data["ticket"]["price"]
  price_rate = 99
  day_in_month = data["ticket"]["date"].day
  day_in_week = data["ticket"]["date"].weekday() + 1
  is_weekday = 0
  if day_in_week == 7:
    is_weekday = 1
  train_data = [[user_id,price,price_rate,day_in_month,day_in_week,int(is_weekday)]]
  print(train_data)
  # 折扣小到大遍历，找到吸引用户购票的最小折扣
  i = 99
  while i >= 10:
    train_data[0][2] = i
    if model.predict(train_data)[0] == 1:
      model.predict(train_data)[0]
      break
    i -= 1

  is_discounted = 0
  discount = 100
  if i >= 10:
    is_discounted = 1
    discount = i
  
  if acc == "12345678910":
    is_discounted = 1
    discount = 50

  return Response({"data":data,"is_discounted":is_discounted,"discount":discount})

@api_view(["get","post"])
def order2(request):
  id_1 = request.GET.get("id1",1891)
  id_2 = request.GET.get("id2",28585)

  acc = request.GET.get("account","13164137913")

  ticket1 = get_one_ticket_info(id_1,acc)
  ticket2 = get_one_ticket_info(id_2,acc)
  data = {
    "ticket1":ticket1,
    "ticket2":ticket2
  }

  return Response({"data":data})

@api_view(["get","post"])
def order_submit(request):
  try:
    tel = request.GET.get("tel","13164137913")
    num = int(request.GET.get("num",1))
    money = request.GET.get("money",None)
    user = User.objects.filter(tel=tel)[0]

    # 普通机票
    if(int(num) == 1):
      id = request.GET.get("id")
      ticket = AoyouTicket.objects.get(id=int(id))
      print(ticket)
      user.user_tickets.add(ticket)
      user.money = user.money - int(money)

    # 中转双机票
    if(int(num) == 2):
      id1 = int(request.GET.get("id1"))
      ticket1 = AoyouTicket.objects.get(id=int(id1))
      print(ticket1)
      user.user_tickets.add(ticket1) 

      id2 = int(request.GET.get("id2"))
      ticket2 = AoyouTicket.objects.get(id=int(id2))
      user.user_tickets.add(ticket2) 
      user.money -= ticket1.price + ticket2.price
    
    user.save()
    return Response({"state":"success"})
  except:
    return Response({"state":"failure"})

@api_view(["get","post"])
def history(request):
  acc = request.GET.get("account","13164137913")

  user = User.objects.filter(Q(email=acc)|Q(tel=acc))[0]
  user_info = User.objects.filter(Q(email=acc)|Q(tel=acc)).values("name","tel","money")[0]

  tickets = user.user_tickets.all().values("id","date","start_time","end_time","start_airport__name",\
        "end_airport__name","airline","catagory","price","discount")

  results = []
  for ticket in tickets:
    duration = compute_duration(ticket["start_time"],ticket["end_time"])
    results.append({
      "ticket": ticket,
      "duration": chinese_time(str(duration)),
      "user_info": user_info,
      "date": chinese_date(ticket["date"])
    })
  
  return Response({"data":results})