from ticket.models import Airport, AoyouTicket
from django.db.models import Q
import re
import datetime
import os

import pandas as pd
from django.conf import settings
from ticket.views.statistic import statistic,get_labels
# noramlly display chinese characters

from rest_framework.decorators import api_view
from rest_framework.response import Response 

def chinese_weekday(value):
  translate = {
    "0":"一",
    "1":"二",
    "2":"三",
    "3":"四",
    "4":"五",
    "5":"六",
    "6":"日"
  }
  return translate[str(value)]

# 检查搜索框输入的两个城市名称是否正确
@api_view(["GET","POST"])
def check_keyword(request):
  start = request.GET.get("start","武汉")
  end = request.GET.get("end","西安")
  # 检查两个城市是否存在
  airport1 = Airport.objects.filter(city=start).count()
  airport2 = Airport.objects.filter(city=end).count()
  if(airport1 <=0 or airport2 <=0):
    return Response({"state":"failure"})
  else:
    return Response({"state": "sucess"})

# 获取机票、中转方案、可视化数据
@api_view(["GET","POST"])
def search_result(request):
  if request.method == "GET":
    # start = "武汉"
    # end = "西安"
    # date_str = "2021-05-24"
    start = request.GET.get("start","武汉")
    end = request.GET.get("end","西安")
    date_str = request.GET.get("date","2021-05-24")

    

    y,m,d = re.findall(r"^(\d*)-(\d*)-(\d*)$",date_str)[0]
    y,m,d = int(y),int(m),int(d)
    date = datetime.date(year=y,month=m,day=d)
    tickets = AoyouTicket.objects.filter(date=date,start_airport__name__contains=start,end_airport__name__contains=end).order_by("price")

      
    sql_table = AoyouTicket.objects.filter(start_airport__name__contains=start,end_airport__name__contains=end).values("date","price")

    # 数据可视化统计
    labels = get_labels()
    if sql_table.count() >= 1:
      # make data ordered
      data = pd.DataFrame(sql_table,columns=["date","price"])
      data["date"] = data["date"].astype("datetime64[ns]")
      result = data.groupby("date").agg({"price":["max","mean","min"]})

      # split data into three fractions
      x = result.index
      min_y = result[("price","min")].values
      mean_y = result[("price","mean")].values
      max_y = result[("price","max")].values

      
      min_text = statistic(x,min_y)
      mean_text = statistic(x,mean_y)
      max_text = statistic(x,max_y)
    else:
      min_text = None
      mean_text = None
      max_text = None
    
    

    t = tickets.all().values("id","date","start_time","end_time","start_airport__name",\
        "end_airport__name","airline","catagory","price","discount")
    
    # 当没有直达机票时，为用户提供十个中转方案
    num = 10
    if len(t) <= 0:
      t = None
    else:
      num = 3
    trans_case = transferring_cases(start,end,date,num)
    
    data = {
      "start":start,
      "end":end,
      "date_str":date_str,
      "tickets":t,
      "date":date,
      "chinese_weekday": chinese_weekday(str(date.weekday())),
      "statistic":{
        "x": labels,
        "min":min_text,
        "mean":mean_text,
        "max":max_text
      },
      "transferring_cases":trans_case
    }
    return Response({"data":data})

def compute_best_price(start,end,date,num):
  '''
  start: 出发地
  end: 到达地
  return： list[dict{previous,next}]
  '''
  # 拿到出发地为start或者目的地为end的机票
  tickets = AoyouTicket.objects.filter(Q(date=date) & (Q(start_airport__name__contains=start)|Q(end_airport__name__contains=end))).values(
    "id","date","start_time","end_time","start_airport__city","end_airport__city","price"
  )
  data = pd.DataFrame(tickets)
  
  # print(data.head())
  # data.to_csv("transfer_cases.csv",index=False,encoding="utf-8",header=True)
  # # 保存进可以很好处理表格结构的数据的pandas的DataFrame对象中
  # data = pd.read_csv("transfer_cases.csv")
  
  #日期和时间类型转换
  date = pd.to_datetime(data["date"],format="%Y-%m-%d")
  start_time = pd.to_datetime(data["start_time"],format="%H:%M:%S")
  end_time = pd.to_datetime(data["end_time"],format="%H:%M:%S")

  data.loc[:,"date"] = date
  data.loc[:,"start_time"] = start_time
  data.loc[:,"end_time"] = end_time

  # 给小于start_time的end_time加上一天
  def next_day(x):
    if x["end_time"] < x["start_time"]:
        return x["end_time"] + pd.Timedelta(days=1)
    else:
        return x["end_time"]
        
  end_time2 = data.apply(next_day,axis=1)
  data.loc[:,"end_time"] = end_time2

  # 将先后两次旅程乘坐的机票分开
  pk_tickets = data.loc[data["start_airport__city"] == start,:]
  sh_tickets = data.loc[data["end_airport__city"] == end,:]

  # 两次能够衔接的机票合并
  merging_result = pd.merge(left=pk_tickets,right=sh_tickets,how="inner",left_on="end_airport__city",
                         right_on="start_airport__city",suffixes=("_1","_2"))

  # 过滤掉哪些前段到达时间与后段起飞时间小于一个小时的机票
  # 过滤掉中间等待时间大于3个小时的机票                      
  one_hour = pd.Timedelta(hours=1)
  result = merging_result.loc[merging_result["end_time_1"] + one_hour <= merging_result["start_time_2"],:]
  result2  = result.loc[result["end_time_1"] + one_hour*3 >=  result["start_time_2"],:]

  # 计算价格时间成本
  def compute_cost(x):
    price1 = x["price_1"]
    price2 = x["price_2"]
    duration = x["end_time_2"] - x["start_time_1"] 
    cost = price1 + price2 + int((duration.total_seconds() / 60 - 60) * 2)
    return cost
  # 增加一列——成本（时间+价格）
  cost_column = result2.apply(compute_cost,axis=1)
  result2["cost"] = cost_column
  # 拿到安装时间价格成本排序的结果
  result3 = result2.sort_values("cost")
  count = result3.shape[0]

  cases = []

  for i in range(num):
    if i >= count:
      break
    r = result3.iloc[i,:]
    cases.append({"previous":int(r["id_1"]),"next":int(r["id_2"])})
  
  return cases

def transferring_cases(start,end,date,num):
  # cases = [
  #   {"previous":	6535,"next":	28585},
  #   {"previous":	6535,"next":	28585},
  #   {"previous":	6535,"next":	28585},
  # ]
  # date = datetime.date(year=2021,month=5,day=23)
  cases = compute_best_price(start,end,date,num)
  c = []
  for case in cases:
    prev = AoyouTicket.objects.filter(id=case["previous"]).values("id","start_time","end_time","start_airport__name",\
        "end_airport__name","price")[0]
    nt = AoyouTicket.objects.filter(id=case["next"]).values("id","start_time","end_time","start_airport__name",\
        "end_airport__name","price")[0]
    c.append({
      "previous":prev,
      "next":nt
    })
  return c